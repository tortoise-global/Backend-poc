# STEP-1

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

bucket_name: turtil-analytics  //(it will ask name in terminal or commandprompt when we run Terraform commands i.e Terraform init, Terraform apply ).

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

## Check Aws Console 


<img width="1440" alt="Screenshot 2024-07-26 at 6 43 45 AM" src="https://github.com/user-attachments/assets/44f6b2b8-1002-4352-9d0e-e4b103620ed7">




### Note: You can create S3-bucket for step-1 by following above s3 configuration or You can create a S3-bucket in aws console.


# STEP-2

## How To Create A Lambda And Store DynamoDb table Data In S3 Bucket

## Creation Of Lambda 

### modeles/lambda/main.tf


```
module "lambda_bucket_name" {
  source            = "../utils"
  random_pet_prefix = "lambda"
  random_pet_length = 2
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket        = module.lambda_bucket_name.resource_id
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "lambda_bucket" {
  bucket                  = aws_s3_bucket.lambda_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_lambda_function" "lambda_function" {
  function_name    = var.lambda_function_prefix
  s3_bucket        = aws_s3_bucket.lambda_bucket.id
  s3_key           = aws_s3_object.lambda_code.key
  runtime          = lookup(var.lambda_runtime, terraform.workspace)
  handler          = lookup(var.lambda_handler, terraform.workspace)
  source_code_hash = data.archive_file.lambda_code.output_base64sha256
  role             = var.role_arn
  timeout          = lookup(var.lambda_timeout, terraform.workspace)
  // Attach Lambda Layer
  layers = var.layers

  # Environment variables if any.
  dynamic "environment" {
    for_each = length(keys(var.shared_environment_variables)) > 0 || length(keys(var.lambda_environment_variables)) > 0 ? [1] : []
    content {
      variables = merge(var.shared_environment_variables, var.lambda_environment_variables)
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_function.function_name}"
  retention_in_days = lookup(var.log_retention, terraform.workspace)
}

data "archive_file" "lambda_code" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${var.output_path_prefix}/lambda_code.zip"
}

resource "aws_s3_object" "lambda_code" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = lookup(var.lambda_s3_keys, terraform.workspace)
  source = data.archive_file.lambda_code.output_path
  etag   = filemd5(data.archive_file.lambda_code.output_path)
}

output "function_name" {
  value = aws_lambda_function.lambda_function.function_name
}

output "log_group_name" {
  value = aws_cloudwatch_log_group.lambda_log_group.name
}

```

### modeles/lambda/outputs.tf


```
output "lambda_bucket_id" {
  value = aws_s3_bucket.lambda_bucket.id
}

output "lambda_arn" {
  value = aws_lambda_function.lambda_function.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.lambda_function.function_name
}

output "lambda_function_arn"{
  value = aws_lambda_function.lambda_function.arn
}

output "lambda_log_group_name" {
  value = aws_cloudwatch_log_group.lambda_log_group.name
}
```

### modeles/lambda/variables.tf


```
variable "lambda_function_name" {
  description = "Name of the Lambda function"

  type = map(string)

  default = {
    "dev"  = "DEV-USER-MANAGEMENT-TURTIL-APP"
    "prod" = "PROD-USER-MANAGEMENT-TURTIL-APP"
  }
}


variable "lambda_runtime" {
  description = "Runtime for the Lambda function"
  type        = map(string)

  default = {
    "dev"  = "python3.11"
    "prod" = "python3.11"
  }
}


variable "lambda_handler" {
  //type    = string
  //default = "lambda_fun.lambda_handler"

  type = map(string)

  default = {
    "dev"  = "lambda_fun.lambda_handler"
    "prod" = "lambda_fun.lambda_handler"
  }
}

variable "lambda_timeout" {
  //type    = number
  //default = 600

  type = map(number)

  default = {
    "dev"  = 600
    "prod" = 600
  }
}

variable "source_dir" {
  description = "Directory containing the Lambda function source code"
  type        = string
}

variable "output_path_prefix" {
  description = "Prefix for the output path of the zipped Lambda code"
  type        = string
}


variable "lambda_s3_keys" {
  description = "S3 key for the Lambda function code"
  type        = map(string)
  default = {
    "dev"  = "DEV-USER-MANAGEMENT-LAMBDA.zip"
    "prod" = "PROD-USER-MANAGEMENT-LAMBDA.zip"
  }
}

variable "role_arn" {
  description = "ARN of the IAM role for the Lambda function"
  type        = string
}


variable "log_retention" {
  //type    = number
  //default = 14

  type = map(number)

  default = {
    "dev"  = 14
    "prod" = 14
  }
}

variable "layers" {
  description = "List of Lambda layers"
  type        = list(string)
  default     = []
}


variable "lambda_function_prefix" {
  description = "Prefix for the Lambda function name"
  type        = string
  default     = "lambda-func"
}

variable "shared_environment_variables" {
  description = "Shared environment variables for all Lambda functions"
  type        = map(string)
  default     = {}
}

variable "lambda_environment_variables" {
  description = "Lambda-specific environment variables"
  type        = map(string)
  default     = {}
}

```


### modeles/lambda/utils/outputs.tf


```
output "resource_id" {
  value = random_pet.resource_name.id
}

```


### modeles/lambda/utils/randompet.tf


```
resource "random_pet" "resource_name" {
  prefix = var.random_pet_prefix
  length = var.random_pet_length
}

```


### modeles/lambda/utils/variables.tf


```
variable "random_pet_prefix" {
  description = "Prefix for the random pet resource"
  type        = string
  default     = "resource"
}

variable "random_pet_length" {
  description = "Length of the random pet suffix"
  type        = number
  default     = 2
}

```


### my-terraform-files/lambda-iam.tf


```


data "aws_iam_policy_document" "comprehensive_policy_document" {
  statement {
    actions = ["logs:*"]
    resources = ["*"]
    effect = "Allow"
  }

  statement {
    actions = ["s3:*"]
    resources = ["*"]
    effect = "Allow"
  }

  statement {
    actions = [ "lambda:*", "dynamodb:*", "events:*"]
    resources = ["*"]
    effect = "Allow"
  }

  

  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetBucketLocation"
    ]
    resources = ["*"]
    effect = "Allow"
  }


}

resource "aws_iam_policy" "comprehensive_policy" {
  # name = var.comprehensive_policy_name
  name        = lookup(var.comprehensive_policy_name, terraform.workspace)

  path = "/"
  policy = data.aws_iam_policy_document.comprehensive_policy_document.json
}

resource "aws_iam_role" "CICDS2-TURTIL-APP_STD_lambda_exec" {
  # name = var.lambda_exec_role_name
  name        = lookup(var.lambda_exec_role_name, terraform.workspace)


  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = aws_iam_policy.comprehensive_policy.arn
  role       = aws_iam_role.CICDS2-TURTIL-APP_STD_lambda_exec.name
}
```



###  my-terraform-files/lambda-layesr.tf


```
# Create Lambda Layer
resource "aws_lambda_layer_version" "std_lambda_layer" {
  filename            = "../${path.module}/layers/layer.zip" # Replace with the path to your ZIP file
  layer_name          = "std_turtil_lambda_layer"
  compatible_runtimes = ["python3.11"] # Replace with your desired Python version
}

output "module_path" {
  value = "../${path.module}/layers/layer.zip"
}

```

###  my-terraform-files/lambda.tf


```
 
module "CICDS2-STD-TURTIL-APP-job1" {
  source                       = "./modules/lambda"
  role_arn                     = aws_iam_role.CICDS2-TURTIL-APP_STD_lambda_exec.arn
  source_dir                   = "../${path.module}/JOBS/Analytics-lambda/analytics_every_day_schedule"
  output_path_prefix           = "../${path.module}/JOBS/Analytics-lambda/analytics_every_day_schedule"
  layers                       = [aws_lambda_layer_version.std_lambda_layer.arn]
  lambda_function_prefix       = terraform.workspace == "prod" ? "PROD-STD-ANATYTICS-EVERY-DAY-SCHEDULE" : "DEV-STD-ANATYTICS-EVERY-DAY-SCHEDULE"
   shared_environment_variables = lookup(var.shared_environment_variables, terraform.workspace)
  lambda_environment_variables = lookup(var.scoped_variable_student_doc, terraform.workspace)
}
```

## Store DynamoDb table Data In S3 Bucket

### JOBS/Analytics-lambda/analytics_every_day_schedule/lambda_fun.py


```
import boto3
import json
import datetime




def lambda_handler(event, context):

   
    try:
        res = user_analytics()

        return {
            'statusCode': 200,
            'body': json.dumps('CSV file uploaded successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }




def user_analytics():
    # Initialize AWS clients
    s3 = boto3.client('s3', region_name='ap-south-1')
    dynamodb = boto3.client('dynamodb', region_name='ap-south-1')

    # Define your S3 bucket name
    bucket_name = 'turtil-analytics'
    
    # Fetch data from DynamoDB
    response = dynamodb.scan(TableName='dev_user_stu')
    items = response['Items']
    
    # Check if there are any items in the DynamoDB table
    if not items:
        return {
            'statusCode': 200,
            'body': 'No data found in DynamoDB table.'
        }
    
    users_processed = 0
    
    # Process each item
    for item in items:
        # Extract userId and date
        user_id = item.get('userId', {}).get('S', '')
        
        # Extract date and convert from milliseconds to datetime
        date_ms = item.get('createdAt', {}).get('N')
        if date_ms:
           
            epoch_timestamp = int(date_ms)
            date = datetime.datetime.fromtimestamp(epoch_timestamp)
            formatted_date = date.strftime('%Y-%m-%d')
            
            # Create a dictionary with userId and date
            data = {
                'userId': user_id,
                'date':  formatted_date
            }
            
            # Convert data to JSON
            data_json = json.dumps(data)
            
            # Create the S3 key (path) for this user
            folder_name = 'Users'
            file_name = f"{user_id}.json"
            s3_key = f"{folder_name}/{file_name}"
            
            # Write data to S3
            s3.put_object(Bucket=bucket_name, Key=s3_key, Body=data_json)
            
            users_processed += 1
    
    return {
        'statusCode': 200,
        'body': f'Data for {users_processed} users written to S3 successfully.'
    }


 
```

# STEP-3

## Setup Aws Glue And Aws Anthena

### Setup and configure Of Aws Glue

### In the AWS console, navigate to AWS Glue.
### Click on "Crawlers" in the left sidebar menu.
<img width="1440" alt="Screenshot 2024-07-26 at 7 33 59 AM" src="https://github.com/user-attachments/assets/5e76336c-5c8c-4161-957d-6594d07d5dfc">

### Click on "Create crawler" button.
<img width="1440" alt="Screenshot 2024-07-26 at 7 34 19 AM" src="https://github.com/user-attachments/assets/bc365863-6695-4787-be8b-f9bad598236d">

### Enter a crawler name (in this case, "my-app-user-1") and click "Next".
<img width="1440" alt="Screenshot 2024-07-26 at 7 34 45 AM" src="https://github.com/user-attachments/assets/48ca5209-160b-487d-a74b-ccd5556a02a3">

### Choose the crawler source type. In this case,Click  " Add a data souce".
<img width="1440" alt="Screenshot 2024-07-26 at 7 34 53 AM" src="https://github.com/user-attachments/assets/3c2f5a16-4858-450e-80ce-af71207ad493">

### Choose "S3" as the data store and specify the path to your S3 bucket. Click "Browse S3".
<img width="1440" alt="Screenshot 2024-07-26 at 7 35 00 AM" src="https://github.com/user-attachments/assets/24aa7a6b-54c7-4fef-81cb-3fc802e50706">

### Search your S3 bucket and click your S3 bucket In this case,Click  "turtil-analytics".
<img width="1440" alt="Screenshot 2024-07-26 at 7 35 24 AM" src="https://github.com/user-attachments/assets/c487f2af-c90a-4961-ab56-95dd3aa1e111">

### Choose the S3 Folder Click "Choose". i.e which your Created in your Lambda Function by python code In this case User folder is selected, the code is STEP-2 the path  "JOBS/Analytics-lambda/analytics_every_day_schedule/lambda_fun.py".
<img width="1440" alt="Screenshot 2024-07-26 at 7 35 44 AM" src="https://github.com/user-attachments/assets/e4368a1b-ae16-4922-8c7c-d5a2dbc9eb4d">

### Click " Add a data souce".
<img width="1440" alt="Screenshot 2024-07-26 at 7 35 55 AM" src="https://github.com/user-attachments/assets/c0e2c87f-8995-4831-8747-703300cc04b0">

### Click " Next".
<img width="1440" alt="Screenshot 2024-07-26 at 7 36 02 AM" src="https://github.com/user-attachments/assets/75e57350-1f53-4aa5-b3e0-9a40b5da1725">


### Click on "New Im Role".
<img width="1440" alt="Screenshot 2024-07-26 at 7 36 17 AM" src="https://github.com/user-attachments/assets/fd700dc6-84c7-4623-a920-0eff64a37831">

### Give your "New Im Role Name" click "create".
<img width="1440" alt="Screenshot 2024-07-26 at 7 37 53 AM" src="https://github.com/user-attachments/assets/681806b4-433f-4edf-9ed3-3a9dd89bc6d5">

### Click on "Next".
<img width="1440" alt="Screenshot 2024-07-26 at 7 38 07 AM" src="https://github.com/user-attachments/assets/39952da0-e133-4a0e-84e4-252edeca8d1e">

### Click on "Add Data Base".
<img width="1440" alt="Screenshot 2024-07-26 at 7 38 51 AM" src="https://github.com/user-attachments/assets/99330615-e713-47ea-b550-d87fae6726d6">

### Give Your  "Add Data Base" Click on "Create Data Base".
<img width="1440" alt="Screenshot 2024-07-26 at 7 39 15 AM" src="https://github.com/user-attachments/assets/2e5d687b-c5f3-44e1-9272-7982a219d611">


<img width="1440" alt="Screenshot 2024-07-26 at 7 39 39 AM" src="https://github.com/user-attachments/assets/3cf9a021-cb9f-45e0-96e2-d440d293e6a1">


<img width="1440" alt="Screenshot 2024-07-26 at 7 39 50 AM" src="https://github.com/user-attachments/assets/e5f38330-ce3c-4c2d-96db-196593be29f9">


<img width="1440" alt="Screenshot 2024-07-26 at 7 40 03 AM" src="https://github.com/user-attachments/assets/e855d455-a9e4-4e78-8acc-3b0298e7b44e">


<img width="1440" alt="Screenshot 2024-07-26 at 7 40 12 AM" src="https://github.com/user-attachments/assets/1eea79ce-be20-4188-90bb-47fab7aa663b">


<img width="1440" alt="Screenshot 2024-07-26 at 7 43 41 AM" src="https://github.com/user-attachments/assets/4932f6ad-feba-4375-83ae-0f7f9ca2ff55">


<img width="1440" alt="Screenshot 2024-07-26 at 7 43 54 AM" src="https://github.com/user-attachments/assets/4457eda2-fef3-45ae-8b83-eec32f0c3c0a">


<img width="1440" alt="Screenshot 2024-07-26 at 7 44 19 AM" src="https://github.com/user-attachments/assets/1feb7620-4f3a-48a0-b981-7599993c4328">


<img width="1440" alt="Screenshot 2024-07-26 at 7 44 29 AM" src="https://github.com/user-attachments/assets/05d28633-d179-47d0-b148-046159a318d6">


<img width="1440" alt="Screenshot 2024-07-26 at 7 44 49 AM" src="https://github.com/user-attachments/assets/da741280-4d98-4ede-bd7d-4259b9905fcf">


<img width="1440" alt="Screenshot 2024-07-26 at 7 44 54 AM" src="https://github.com/user-attachments/assets/de6734fc-763c-41c2-84f3-ce7e62724ca0">









