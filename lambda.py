import json

def lambda_handler(event, context):
    print("hello")
    message = {
    'message': 'Execution started successfully!'
    }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(message)
    }