import boto3

# Initialize the boto3 client for API Gateway and Lambda
apigateway_client = boto3.client('apigateway')
lambda_client = boto3.client('lambda')

# Create the API Gateway
api_response = apigateway_client.create_rest_api(
    name='hackathon-aws-creds',
    description='API for hackathon AWS credentials',
    endpointConfiguration={
        'types': ['REGIONAL']
    }
)

api_id = api_response['id']

# Get the root resource id
resources = apigateway_client.get_resources(restApiId=api_id)
root_id = next(item['id'] for item in resources['items'] if item['path'] == '/')

# Create a resource for the Lambda function
resource_response = apigateway_client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='hackathon_sts_token'
)

resource_id = resource_response['id']

# Create a POST method for the resource
apigateway_client.put_method(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)

# Get the Lambda function ARN
lambda_function_name = 'hackathon_sts_token'
lambda_response = lambda_client.get_function(FunctionName=lambda_function_name)
lambda_arn = lambda_response['Configuration']['FunctionArn']

# Create the Lambda integration
apigateway_client.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='POST',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f'arn:aws:apigateway:{boto3.Session().region_name}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
)

# Grant API Gateway permission to invoke the Lambda function
lambda_client.add_permission(
    FunctionName=lambda_function_name,
    StatementId='apigateway-invoke-permissions',
    Action='lambda:InvokeFunction',
    Principal='apigateway.amazonaws.com',
    SourceArn=f'arn:aws:execute-api:{boto3.Session().region_name}:{boto3.client("sts").get_caller_identity()["Account"]}:{api_id}/*/POST/hackathon_sts_token'
)

print(f"API Gateway created with ID: {api_id}")
