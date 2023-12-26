# Terraform Infrastructure Deployment


## Terraform S3 Bucket Configuration
This Terraform script sets up an AWS S3 bucket with versioning enabled and server-side encryption configured for storing Terraform state files. The script also includes a validation for the bucket name.

## Prerequisites
Before running this Terraform script, ensure you have:

AWS credentials configured with necessary permissions.
Terraform installed on your local machine.
Usage
Clone this repository to your local machine.
Navigate to the directory containing the Terraform files.
Configuration
Modify the variables.tf file to set your desired configurations:

bucket_name: Remote S3 bucket name. Ensure it follows S3 naming rules.
Terraform Initialization
Run the following commands to initialize the Terraform workspace:


## Terraform Resources

## S3 Configure

### s3bucket.tf

```

# S3 Bucket for TF State File
resource "aws_s3_bucket" "terraform_state" {
  bucket        = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "terraform_bucket_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_crypto_conf" {
  bucket = aws_s3_bucket.terraform_state.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

```

## variables.tf

```
variable "bucket_name" {
  description = "Remote S3 Bucket Name"
  type        = string
  validation {
    condition     = can(regex("^([a-z0-9]{1}[a-z0-9-]{1,61}[a-z0-9]{1})$", var.bucket_name))
    error_message = "Bucket Name must not be empty and must follow S3 naming rules."
  }
}

```


## S3 Bucket for Terraform State
Creates an AWS S3 bucket to store Terraform state files.

```
resource "aws_s3_bucket" "terraform_state" {
  bucket        = var.bucket_name
  force_destroy = true
}
```

## S3 Bucket Versioning
Enables versioning for the created S3 bucket.

```
resource "aws_s3_bucket_versioning" "terraform_bucket_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

## S3 Bucket Server-Side Encryption
Configures server-side encryption for the S3 bucket.

```
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_crypto_conf" {
  bucket = aws_s3_bucket.terraform_state.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

## Defines the bucket_name

```
variable "bucket_name" {
  description = "Remote S3 Bucket Name"
  type        = string
  validation {
    condition     = can(regex("^([a-z0-9]{1}[a-z0-9-]{1,61}[a-z0-9]{1})$", var.bucket_name))
    error_message = "Bucket Name must not be empty and must follow S3 naming rules."
  }
}

```

## Defines the variables used in the Terraform configuration:

bucket_name: tf-state-backend-ci-cd  //(it will ask name in terminal or commandprompt when we run Terraform commands i.e Terraform init, Terraform apply ).

## Terraform Initialization
Run the following commands to initialize the Terraform workspace:

```
terraform init

```

## Terraform Deployment
Execute the following command to apply the configuration:

```
terraform apply

```

### Note: You can create S3-bucket for step-1 by following above s3 configuration or You can create a S3-bucket in aws console.



# STEP-1:

This Terraform configuration script is designed to provision AWS resources using the AWS provider and manage state using an S3 backend.

## Overview

The Terraform configuration is divided into two phases:

1. **Local Backend Provisioning**: Initially, the backend configuration is commented out, allowing you to provision resources using a local backend (state stored locally). This phase is intended for setting up basic infrastructure resources like Buckets and Tables.
   
2. **AWS S3 Backend Configuration**: After the initial resources are created, the backend configuration needs to be uncommented. This phase configures Terraform to store its state in an S3 bucket, enabling remote state management.
   
## Prerequisites

- **Terraform Installed**: Ensure you have Terraform installed locally. You can download it from [Terraform's official website](https://www.terraform.io/downloads.html).
- **AWS Account**: You need an AWS account with appropriate permissions to create and manage resources.

## Configuration Details

### Backend Configuration

### main.tf

```
terraform {
  # Run init/plan/apply with "backend" commented-out (ueses local backend) to provision Resources (Bucket, Table)
  # Then uncomment "backend" and run init, apply after Resources have been created (uses AWS)
  backend "s3" {
    bucket         = "tf-state-backend-ci-cd"
    key            = "tf-infra/terraform.tfstate"
    region         = "ap-south-1"
  }

}


provider "aws" {
  region = "us-east-1"
}

```

Initially, the backend configuration is commented out to allow local backend usage:

```hcl
terraform {
  # Run init/plan/apply with "backend" commented-out (uses local backend) to provision Resources (Bucket, Table)
  # Then uncomment "backend" and run init, apply after Resources have been created (uses AWS)
  backend "s3" {
    bucket         = "tf-state-backend-ci-cd"
    key            = "tf-infra/terraform.tfstate"
    region         = "ap-south-1"
    //dynamodb_table = "terraform-state-locking"
    //encrypt        = true
  }
}
```
Uncomment the backend block after provisioning the initial resources locally to switch to an AWS S3 backend. Make sure to provide the correct AWS credentials and access to the specified bucket and DynamoDB table (for state locking).

AWS Provider Configuration
The AWS provider block specifies the region to be used for provisioning resources:

```
provider "aws" {
  region = "us-east-1"
}
```
Make sure to update the region field with the desired AWS region.

Usage
Follow these steps to deploy the infrastructure:

### Local Backend Provisioning:

Comment out the backend configuration in the Terraform file.
Run the following commands:
```
terraform init
terraform plan
terraform apply
```
### AWS S3 Backend Configuration:

Uncomment the backend configuration in the Terraform file.
Run the following commands:
```
terraform init
terraform apply
```


# STEP-2:

# AWS DynamoDB Terraform Configuration

```

resource "aws_dynamodb_table" "post" {
  name           = "post"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "postid"
    type = "S"
  }
  

  hash_key = "postid"

}

```

This repository contains Terraform configurations to create AWS DynamoDB tables for various purposes.

## Table Definitions

### Post Table

The `post` table configuration is specified as:

- **Name**: `post`
- **Billing Mode**: `PAY_PER_REQUEST`
- **Attributes**:
  - `postid`:
    - Type: `String (S)`
- **Key Schema**:
  - Hash Key: `postid`

## Usage

To utilize these configurations, ensure you have Terraform installed and configured with appropriate AWS credentials.

1. Clone this repository.
2. Modify the configuration files as needed.
3. Run `terraform init` to initialize the working directory.
4. Execute `terraform plan` to review the changes that will be applied.
5. Run `terraform apply` to create the DynamoDB tables in your AWS account.

## Notes

- Ensure proper AWS IAM credentials and permissions are set for the Terraform execution.
- Review and modify the configurations based on your specific requirements before applying changes to your AWS account.

# STEP-3 :

# AWS Lambda Function Deployment with Terraform

This Terraform script deploys an AWS Lambda function along with required resources to support its execution.

## Overview

## Lambda configurations:

```
resource "random_pet" "lambda_bucket_name" {
  prefix = "lambda"
  length = 2
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket        = random_pet.lambda_bucket_name.id
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}




resource "aws_iam_role" "BACKEND-POC_lambda_exec" {
  name = "BACKEND-POC-lambda"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "BACKEND-POC_lambda_policy" {
  role       = aws_iam_role.BACKEND-POC_lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "BACKEND-POC" {
  function_name = "BACKEND-POC"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_BACKEND-POC.key

  runtime = "python3.11"
  handler = "function.lambda_handler"

  source_code_hash = data.archive_file.lambda_BACKEND-POC.output_base64sha256

  role = aws_iam_role.BACKEND-POC_lambda_exec.arn
}

resource "aws_cloudwatch_log_group" "BACKEND-POC" {
  name = "/aws/lambda/${aws_lambda_function.BACKEND-POC.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_BACKEND-POC" {
  type = "zip"

  source_file  = "function.py"
  output_path = "BACKEND-POC.zip"
}

resource "aws_s3_object" "lambda_BACKEND-POC" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "BACKEND-POC.zip"
  source = data.archive_file.lambda_BACKEND-POC.output_path

  etag = filemd5(data.archive_file.lambda_BACKEND-POC.output_path)
}


resource "aws_iam_policy" "dynamodb_policy" {
  name        = "DynamoDBPolicy"
  description = "Policy allowing basic DynamoDB operations"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ],
        Resource = "arn:aws:dynamodb:*:*:table/*" // Replace with specific table ARNs if needed
      }
    ]
  })
}

# Attach policy to Lambda's role
resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  policy_arn = aws_iam_policy.dynamodb_policy.arn
  role       = aws_iam_role.BACKEND-POC_lambda_exec.name

}

```



The infrastructure provisioned includes:

- **Random Pet Name Generation**: Creates a random prefix-based name for the S3 bucket.
- **S3 Bucket for Lambda**: Defines an S3 bucket to store the Lambda function's code.
- **Public Access Block for S3 Bucket**: Restricts public access to the S3 bucket.
- **IAM Role for Lambda Execution**: Grants necessary permissions to the Lambda function for execution.
- **IAM Role Policy Attachment**: Attaches an AWS managed policy to the Lambda execution role.
- **Lambda Function**: Deploys the Lambda function using the specified runtime and handler.
- **CloudWatch Log Group**: Sets up a log group for Lambda function logs.
- **Archive File and S3 Object**: Archives the Lambda function code and uploads it to the S3 bucket.
- **IAM Policy for DynamoDB**: Defines a custom policy allowing basic DynamoDB operations.
- **IAM Policy Attachment to Lambda's Role**: Attaches the DynamoDB policy to the Lambda execution role.

## Terraform Resources

### `random_pet` Resource

Generates a random pet name prefix used for the S3 bucket naming.

```
resource "random_pet" "lambda_bucket_name" {
  prefix = "lambda"
  length = 2
}

```

### `aws_s3_bucket` Resource

Creates an S3 bucket with the random pet name for storing Lambda function code.

```
resource "aws_s3_bucket" "lambda_bucket" {
  bucket        = random_pet.lambda_bucket_name.id
  force_destroy = true
}

```

### `aws_s3_bucket_public_access_block` Resource

Applies public access block settings to the S3 bucket, restricting public access.

```
resource "aws_s3_bucket_public_access_block" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

```

### `aws_iam_role` Resource

Defines an IAM role for Lambda function execution.

```

resource "aws_iam_role" "BACKEND-POC_lambda_exec" {
  name = "BACKEND-POC-lambda"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

```

### `aws_iam_role_policy_attachment` Resource

Attaches an AWS managed policy (`AWSLambdaBasicExecutionRole`) to the Lambda execution role.

```

resource "aws_iam_role_policy_attachment" "BACKEND-POC_lambda_policy" {
  role       = aws_iam_role.BACKEND-POC_lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

```

### `aws_lambda_function` Resource

Deploys the Lambda function using the specified code from the S3 bucket.

```

resource "aws_lambda_function" "BACKEND-POC" {
  function_name = "BACKEND-POC"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_BACKEND-POC.key

  runtime = "python3.11"
  handler = "function.lambda_handler"

  source_code_hash = data.archive_file.lambda_BACKEND-POC.output_base64sha256

  role = aws_iam_role.BACKEND-POC_lambda_exec.arn
}

```

### `aws_cloudwatch_log_group` Resource

Sets up a CloudWatch log group for Lambda function logs.

```

resource "aws_cloudwatch_log_group" "BACKEND-POC" {
  name = "/aws/lambda/${aws_lambda_function.BACKEND-POC.function_name}"

  retention_in_days = 14
}

```

### `data.archive_file` Resource

Archives the Lambda function code and prepares it for upload to the S3 bucket.

```
data "archive_file" "lambda_BACKEND-POC" {
  type = "zip"

  source_file  = "function.py"
  output_path = "BACKEND-POC.zip"
}

```

### `aws_s3_object` Resource

Uploads the archived Lambda function code to the S3 bucket.

```

resource "aws_s3_object" "lambda_BACKEND-POC" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "BACKEND-POC.zip"
  source = data.archive_file.lambda_BACKEND-POC.output_path

  etag = filemd5(data.archive_file.lambda_BACKEND-POC.output_path)
}


```

### `aws_iam_policy` Resource

Creates an IAM policy allowing basic DynamoDB operations.

```

resource "aws_iam_policy" "dynamodb_policy" {
  name        = "DynamoDBPolicy"
  description = "Policy allowing basic DynamoDB operations"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ],
        Resource = "arn:aws:dynamodb:*:*:table/*" // Replace with specific table ARNs if needed
      }
    ]
  })
}

```

### `aws_iam_role_policy_attachment` Resource

Attaches the DynamoDB policy to the Lambda execution role for access to DynamoDB resources.

```

# Attach policy to Lambda's role
resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  policy_arn = aws_iam_policy.dynamodb_policy.arn
  role       = aws_iam_role.BACKEND-POC_lambda_exec.name

}

```

## Usage

1. Ensure you have AWS credentials configured properly on your machine.
2. Install Terraform and initialize the working directory.
3. Customize the variables and resource configurations as needed.
4. Run `terraform init` followed by `terraform apply` to provision the resources.

## Important Note

- Make sure to review and adjust resource configurations according to your specific requirements before applying this Terraform script in a production environment.






# step4

## AWS Cognito User Pool and Client Setup

This Terraform script provisions an AWS Cognito User Pool and a corresponding User Pool Client, setting up authentication mechanisms and configurations for user management.

Prerequisites
Ensure you have the following before executing this Terraform script:

AWS CLI configured with necessary permissions
Terraform installed on your local machine
## Configuration

```

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
 }
}



resource "aws_cognito_user_pool_client" "client" {
  name                            = "cognito-client"
  user_pool_id                    = aws_cognito_user_pool.user_pool.id
  generate_secret                 = false
  refresh_token_validity          = 90
  prevent_user_existence_errors   = "ENABLED"
 // allowed_oauth_flows             = ["code", "implicit", "client_credentials"]  # Updated with correct values
  allowed_oauth_flows             = ["implicit"]  # Updated with correct values

  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes            = ["openid"]
  callback_urls                   = ["https://turtil.raj/callback"]  # Specify your callback URL(s) here
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


```


## The Terraform script consists of three main resources:

### AWS Cognito User Pool
Resource: aws_cognito_user_pool.user_pool

```
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
 }
}

```

Name: "user-pool"

Username Attributes: Email

Auto-verified Attributes: Email

Password Policy:

Minimum Length: 6
(Optional) Uncomment and customize to require lowercase, uppercase, numbers, and symbols in passwords.
Verification Message Template:

Default Email Option: "CONFIRM_WITH_CODE"
Email Subject: "Account Confirmation"
Email Message: "Your confirmation code is {####}"
Schema:

Defines user attributes like email with constraints for length.
<!-- Uncomment below sections for additional attributes like name, phone number, and address -->
<!--
- `name`: "String", Mutable, Required
- `phonenumber`: "String", Mutable, Required
- `address`: "String", Mutable, Required
-->
### AWS Cognito User Pool Client
Resource: aws_cognito_user_pool_client.client

```
resource "aws_cognito_user_pool_client" "client" {
  name                            = "cognito-client"
  user_pool_id                    = aws_cognito_user_pool.user_pool.id
  generate_secret                 = false
  refresh_token_validity          = 90
  prevent_user_existence_errors   = "ENABLED"
 // allowed_oauth_flows             = ["code", "implicit", "client_credentials"]  # Updated with correct values
  allowed_oauth_flows             = ["implicit"]  # Updated with correct values

  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes            = ["openid"]
  callback_urls                   = ["https://turtil.raj/callback"]  # Specify your callback URL(s) here
  explicit_auth_flows             = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]
}


```

Name: "cognito-client"
User Pool ID: Obtained from the created user pool
Generate Secret: Disabled
Refresh Token Validity: 90 days
Error Handling: Enabled to prevent user existence errors
OAuth Flows:
Allowed OAuth Flows: "implicit"
Allowed OAuth Flows User Pool Client: Enabled
OAuth Scopes: OpenID
Callback URLs: Specify your callback URL(s) here
Explicit Auth Flows: Allow Refresh Token Auth, User Password Auth, Admin User Password Auth

### AWS Cognito User Pool Domain
Resource: aws_cognito_user_pool_domain.cognito-domain

```
resource "aws_cognito_user_pool_domain" "cognito-domain" {
  domain       = "turtil"
  user_pool_id = aws_cognito_user_pool.user_pool.id
}

```

Domain: "turtil"
User Pool ID: Obtained from the created user pool

### Usage

```
Clone this repository.
Ensure AWS CLI is properly configured with necessary permissions.
Run terraform init to initialize the working directory.
Run terraform apply to create the AWS resources as defined in the script.
Check the AWS Management Console or command line output for created resources.

```
License
This script is licensed under MIT License.

Contributors
S.Rajsekhar - Role


Acknowledgments

AWS Cognito Documentation

Inspiration from Terraform AWS Provider

For more detailed information, refer to the Terraform Documentation.


# step 5

# AWS API Gateway v2 CUSTOM-DOMAIN Terraform Configuration
This Terraform configuration is designed to set up an AWS API Gateway v2 with TLS certificates, domain names, and API mappings.


## Prerequisites

- AWS CLI installed and configured with necessary permissions.
- Terraform installed locally.

## Setup

1. Clone this repository.
2. Ensure AWS credentials are properly set up in the environment.
3. Modify the `main.tf` file with your specific configurations.

## Configuration Details

```

#create TLS certificate.

resource "aws_acm_certificate" "api" {
  domain_name       = "devapi.turtil.co" //give your own end-point or backend url name (TLS certificate)
  validation_method = "DNS"
}

data "aws_route53_zone" "public" {
  name         = "turtil.co" // give your  own domain name
  private_zone = false
}

resource "aws_route53_record" "api_validation" {
  for_each = {
    for dvo in aws_acm_certificate.api.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.public.zone_id
}

resource "aws_acm_certificate_validation" "api" {
  certificate_arn         = aws_acm_certificate.api.arn
  validation_record_fqdns = [for record in aws_route53_record.api_validation : record.fqdn]
}




# Specify the domain name, which should match the certificate i.e above given TLS certificate(for our case it is devapi.turtil.co)

resource "aws_apigatewayv2_domain_name" "api" {
  domain_name = "devapi.turtil.co"

  domain_name_configuration {
    certificate_arn = aws_acm_certificate.api.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  depends_on = [aws_acm_certificate_validation.api]
}

resource "aws_route53_record" "api" {
  name    = aws_apigatewayv2_domain_name.api.domain_name
  type    = "A"
  zone_id = data.aws_route53_zone.public.zone_id

  alias {
    name                   = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}



#let's create API mapping. The first one is for the base path. And the second one is to map the staging stage with the v1 path.

resource "aws_apigatewayv2_api_mapping" "api" {
  api_id      = aws_apigatewayv2_api.main.id
  domain_name = aws_apigatewayv2_domain_name.api.id
  stage       = aws_apigatewayv2_stage.dev.id
}

resource "aws_apigatewayv2_api_mapping" "api_v1" {
  api_id          = aws_apigatewayv2_api.main.id
  domain_name     = aws_apigatewayv2_domain_name.api.id
  stage           = aws_apigatewayv2_stage.dev.id
  api_mapping_key = "v1"
}

output "custom_domain_api" {
  value = "https://${aws_apigatewayv2_api_mapping.api.domain_name}"
}

output "custom_domain_api_v1" {
  value = "https://${aws_apigatewayv2_api_mapping.api_v1.domain_name}/${aws_apigatewayv2_api_mapping.api_v1.api_mapping_key}"
}




```


### TLS Certificate Creation

- A TLS certificate for `devapi.turtil.co` is created using AWS ACM (Amazon Certificate Manager).
- DNS validation is used to validate the certificate.

  ```
  #create TLS certificate.

    resource "aws_acm_certificate" "api" {
      domain_name       = "devapi.turtil.co" //give your own end-point or backend url name (TLS certificate)
      validation_method = "DNS"
    }

  ```

### Route 53 Configuration

- A Route 53 zone for `turtil.co` (public domain) is utilized for DNS validation.
- Route 53 records are created for ACM certificate validation.

  ```
  data "aws_route53_zone" "public" {
  name         = "turtil.co" // give your  own domain name
  private_zone = false
  }
  
  resource "aws_route53_record" "api_validation" {
    for_each = {
      for dvo in aws_acm_certificate.api.domain_validation_options : dvo.domain_name => {
        name   = dvo.resource_record_name
        record = dvo.resource_record_value
        type   = dvo.resource_record_type
      }
    }
  
    allow_overwrite = true
    name            = each.value.name
    records         = [each.value.record]
    ttl             = 60
    type            = each.value.type
    zone_id         = data.aws_route53_zone.public.zone_id
  }
  
  resource "aws_acm_certificate_validation" "api" {
    certificate_arn         = aws_acm_certificate.api.arn
    validation_record_fqdns = [for record in aws_route53_record.api_validation : record.fqdn]
  }

  ```

### API Gateway Configuration

- An API Gateway domain name `devapi.turtil.co` is set up.
- This domain name is associated with the ACM TLS certificate for secure communication.
- The security policy is enforced to TLS 1.2.

  ```
  # Specify the domain name, which should match the certificate i.e above given TLS certificate(for our case it is devapi.turtil.co)

  resource "aws_apigatewayv2_domain_name" "api" {
    domain_name = "devapi.turtil.co"
  
    domain_name_configuration {
      certificate_arn = aws_acm_certificate.api.arn
      endpoint_type   = "REGIONAL"
      security_policy = "TLS_1_2"
    }
  
    depends_on = [aws_acm_certificate_validation.api]
  }
  
  resource "aws_route53_record" "api" {
    name    = aws_apigatewayv2_domain_name.api.domain_name
    type    = "A"
    zone_id = data.aws_route53_zone.public.zone_id
  
    alias {
      name                   = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].target_domain_name
      zone_id                = aws_apigatewayv2_domain_name.api.domain_name_configuration[0].hosted_zone_id
      evaluate_target_health = false
    }
  }

  ```

### API Mapping

- Two API mappings are created:
  - The first mapping is for the base path of the API.
  - The second mapping directs the `v1` path to the `staging` stage of the API.
 
    ```
        
    #let's create API mapping. The first one is for the base path. And the second one is to map the staging stage with the v1 path.
    
    resource "aws_apigatewayv2_api_mapping" "api" {
      api_id      = aws_apigatewayv2_api.main.id
      domain_name = aws_apigatewayv2_domain_name.api.id
      stage       = aws_apigatewayv2_stage.dev.id
    }
    
    resource "aws_apigatewayv2_api_mapping" "api_v1" {
      api_id          = aws_apigatewayv2_api.main.id
      domain_name     = aws_apigatewayv2_domain_name.api.id
      stage           = aws_apigatewayv2_stage.dev.id
      api_mapping_key = "v1"
    }
    
    output "custom_domain_api" {
      value = "https://${aws_apigatewayv2_api_mapping.api.domain_name}"
    }
    
    output "custom_domain_api_v1" {
      value = "https://${aws_apigatewayv2_api_mapping.api_v1.domain_name}/${aws_apigatewayv2_api_mapping.api_v1.api_mapping_key}"
    }
    
    ```
    

## Usage

1. Run `terraform init` to initialize the Terraform configuration.
2. Run `terraform plan` to review the changes that will be applied.
3. Run `terraform apply` to apply the changes and create the infrastructure.
4. Check the AWS Management Console to verify the setup.

## Outputs

- `custom_domain_api`: Provides the URL for accessing the base path of the API.
- `custom_domain_api_v1`: Provides the URL for accessing the `v1` path of the API.

## Clean Up

To remove the created resources:

1. Run `terraform destroy` to delete all the resources provisioned by this Terraform configuration.
2. Confirm the deletion when prompted.

## Notes

- Ensure proper permissions and configurations are set to avoid any issues during resource creation and management.
- Review and modify the Terraform code according to specific requirements and security best practices.



