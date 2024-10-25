provider "aws" {
    region = "us-west-2"
}

resource "aws_lambda_function" "example" {
    filename         = "lambda_function_payload.zip"
    function_name    = "example_lambda_function"
    role             = aws_iam_role.lambda_exec.arn
    handler          = "index.handler"
    source_code_hash = filebase64sha256("lambda_function_payload.zip")
    runtime          = "nodejs14.x"
}

resource "aws_iam_role" "lambda_exec" {
    name = "lambda_exec_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Sid    = ""
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
            },
        ]
    })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
    role       = aws_iam_role.lambda_exec.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_api_gateway_rest_api" "example" {
    name        = "example-api"
    description = "Example API Gateway"
}

resource "aws_api_gateway_resource" "example" {
    rest_api_id = aws_api_gateway_rest_api.example.id
    parent_id   = aws_api_gateway_rest_api.example.root_resource_id
    path_part   = "example"
}

resource "aws_api_gateway_method" "example" {
    rest_api_id   = aws_api_gateway_rest_api.example.id
    resource_id   = aws_api_gateway_resource.example.id
    http_method   = "GET"
    authorization = "NONE"
}

resource "aws_api_gateway_integration" "example" {
    rest_api_id = aws_api_gateway_rest_api.example.id
    resource_id = aws_api_gateway_resource.example.id
    http_method = aws_api_gateway_method.example.http_method
    type        = "AWS_PROXY"
    integration_http_method = "POST"
    uri         = aws_lambda_function.example.invoke_arn
}

resource "aws_lambda_permission" "apigw" {
    statement_id  = "AllowAPIGatewayInvoke"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.example.function_name
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${aws_api_gateway_rest_api.example.execution_arn}/*/*"
}
