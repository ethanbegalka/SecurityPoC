from aws_cdk import (
    aws_iam as iam,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    core
)

import re
import path
import os
import sys
import subprocess

if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile


from policy_sentry.querying.actions import get_actions_with_access_level


class SecurityPoCStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # LAMBDA FUNCTION CREATION

        zipfile.ZipFile('my-lambda-handler.zip', mode='w').write("lambda.py")
        print("Zipfile has been created")

        securitypoc_lambda = lambda_.Function(self, "securitypoc_lambda",
            code=lambda_.Code.from_asset(os.getcwd() + "\my-lambda-handler.zip"),
            handler="lambda.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_6
        )

        # API GATEWAY CREATION

        api_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(effect= 
                    iam.Effect.ALLOW,
                    principals=[
                        iam.AccountPrincipal("233105232672"),
                    ],
                    actions= [
                        "execute-api:Invoke"
                    ],
                    resources=["*"])
            ],
        )

        securitypoc_api = apigateway.LambdaRestApi(self, "securitypoc_apigateway",
            handler=securitypoc_lambda,
            policy=api_policy
        )

        # API GATEWAY ACCESS ROLE
        
        cmd = ["aws","configure","get","region"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        current_region = str(result.stdout.decode('utf-8'))[:-2]

        apiresourcearn = "arn:aws:apigateway:{}::/restapis/{}/resources/{}/methods/GET".format(
            current_region,
            securitypoc_api.rest_api_id,
            securitypoc_api.rest_api_root_resource_id
        )

        securitypoc_role_policy = iam.ManagedPolicy(
            self, "SecurityPoCRolePolicy",
            managed_policy_name="SecurityPoCRolePolicy",
            statements=[
                iam.PolicyStatement(effect= 
                    iam.Effect.ALLOW,
                    actions= [
                        "apigateway:POST",
                        "execute-api:Invoke"
                    ],
                    resources=[
                        securitypoc_api.arn_for_execute_api(),
                        apiresourcearn
                    ])
            ],
        )

        roledict = {
            "name": "SecurityPoCRole",
            "policies": [securitypoc_role_policy],
            "permissions_boundary": None,
        }

        securitypoc_role = iam.Role(
            self, roledict["name"], 
            assumed_by=iam.AccountPrincipal('899456967600'),
            description=roledict["name"] + "description", 
            external_id=None, 
            external_ids=None, 
            inline_policies=None, 
            managed_policies=roledict["policies"],
            max_session_duration=core.Duration.hours(12),
            path=None,
            permissions_boundary=roledict["permissions_boundary"], 
            role_name=roledict["name"]
        )