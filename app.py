#!/usr/bin/env python3

from aws_cdk import core

from securitypoc.securitypoc_stack import SecurityPoCStack


app = core.App()
SecurityPoCStack(app, "securitypoc")

app.synth()
