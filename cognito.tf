
/*
// Resources
resource "aws_cognito_user_pool" "user_pool" {
  name = "user-pool"

  username_attributes = ["email"]
  auto_verified_attributes = ["email"]
  password_policy {
    minimum_length = 6
    //require_lowercase = true
    //require_numbers   = true
   // require_symbols   = true
   // require_uppercase = true
  }

  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_subject        = "Account Confirmation"
    email_message        = "Your confirmation code is {####}"
  }

  schema {
    name     = "email"
    attribute_data_type = "String"
    required = true
    mutable  = true

    string_attribute_constraints {
      min_length = 1
      max_length = 256
    }
*/
/*
    schema {
    name = "name"
    attribute_data_type = "String"
    mutable = true
    required = true
  }

  schema {
    name = "phonenumber"
    attribute_data_type = "String"
    mutable = true
    required = true
  }

  schema {
    name = "address"
    attribute_data_type = "String"
    mutable = true
    required = true
  }
*/

 // }
//}
/*
resource "aws_cognito_user_pool_client" "client" {
  name                            = "cognito-client"
  user_pool_id                    = aws_cognito_user_pool.user_pool.id
  generate_secret                 = false
  refresh_token_validity          = 90
  prevent_user_existence_errors   = "ENABLED"
  allowed_oauth_flows             = ["refresh_token", "password", "admin_user_password"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes            = ["openid"]
  explicit_auth_flows             = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]
}
*/
/*
resource "aws_cognito_user_pool_client" "client" {
  name                            = "cognito-client"
  user_pool_id                    = aws_cognito_user_pool.user_pool.id
  generate_secret                 = false
  refresh_token_validity          = 90
  prevent_user_existence_errors   = "ENABLED"
  allowed_oauth_flows             = ["code", "implicit", "client_credentials"]  # Updated with correct values
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes            = ["openid"]
  explicit_auth_flows             = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]
}

resource "aws_cognito_user_pool_domain" "cognito-domain" {
  domain       = "turtil"
  user_pool_id = aws_cognito_user_pool.user_pool.id
}
*/