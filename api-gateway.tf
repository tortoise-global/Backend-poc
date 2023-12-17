resource "aws_apigatewayv2_api" "main" {
  name          = "main"  // give your own name
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "dev" {
  api_id = aws_apigatewayv2_api.main.id

  name        = "dev" // give your own name
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.main_api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_cloudwatch_log_group" "main_api_gw" {
  name = "/aws/api-gw/${aws_apigatewayv2_api.main.name}"

  retention_in_days = 14
}

variable "AWS_REGION" {
  description = "The AWS region where resources will be deployed"
  default     = "us-east-1"  # Set your preferred default AWS region here
}

/*
resource "aws_apigatewayv2_authorizer" "cognito_authorizer" {
  api_id             = aws_apigatewayv2_api.main.id
  name               = "cognito-authorizer"
  authorizer_type    = "JWT"
  identity_sources   = ["$request.header.Authorization"]
  jwt_configuration {
    issuer             = "https://cognito-idp.${var.AWS_REGION}.amazonaws.com/${aws_cognito_user_pool.user_pool.id}"
    audience           = [aws_cognito_user_pool_client.client.id]
  }
}


resource "aws_apigatewayv2_authorizer" "cognito_authorizer" {
  api_id             = aws_apigatewayv2_api.main.id
  name               = "cognito-authorizer"
  authorizer_type    = "JWT"
  identity_sources   = ["$request.header.Authorization"]
  jwt_configuration {
    issuer             = "https://cognito-idp.<your-region>.amazonaws.com/${aws_cognito_user_pool.user_pool.id}"
    audience           = [aws_cognito_user_pool_client.client.id]
  }
}
*/





resource "aws_apigatewayv2_integration" "lambda_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.BACKEND-POC.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_authorizer" "cognito_authorizer" {
  api_id             = aws_apigatewayv2_api.main.id
  name               = "cognito-authorizer"
  authorizer_type    = "JWT"
  identity_sources   = ["$request.header.Authorization"]  # Assuming JWT token is in the Authorization header
  jwt_configuration {
    issuer             = "https://cognito-idp.${var.AWS_REGION}.amazonaws.com/${aws_cognito_user_pool.user_pool.id}"
    audience           = [aws_cognito_user_pool_client.client.id]
  }
}

resource "aws_apigatewayv2_route" "get_BACKEND-POC" {
  api_id        = aws_apigatewayv2_api.main.id
  route_key     = "GET /allpost"
  target        = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
  authorizer_type    = "JWT"
  authorization_scopes = ["openid"]  # Set the required scopes for authorization
  authorizer_id        = aws_apigatewayv2_authorizer.cognito_authorizer.id
}


/*
resource "aws_apigatewayv2_route" "get_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /allpost" // give your own endpoint name in place of allpost
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"

  authorization_scopes = ["openid"]  # Set the required scopes for authorization
  authorizer_id = aws_apigatewayv2_authorizer.cognito_authorizer.id
}
*/

resource "aws_apigatewayv2_route" "post_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /addpost" // give your own endpoint name in place of addpost
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}




resource "aws_apigatewayv2_route" "deletepost_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "DELETE /deletepostbypostid"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}


resource "aws_apigatewayv2_route" "addsignup_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /addsignup"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}


resource "aws_apigatewayv2_route" "get_token_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /get_token" // give your own endpoint name in place of allpost
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}



resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.BACKEND-POC.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

output "BACKEND-POC_base_url" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}
