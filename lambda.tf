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
  handler = "function.handler"

  source_code_hash = data.archive_file.lambda_BACKEND-POC.output_base64sha256

  role = aws_iam_role.BACKEND-POC_lambda_exec.arn
}

resource "aws_cloudwatch_log_group" "BACKEND-POC" {
  name = "/aws/lambda/${aws_lambda_function.BACKEND-POC.function_name}"

  retention_in_days = 14
}

data "archive_file" "lambda_BACKEND-POC" {
  type = "zip"

  source_dir  = "../${path.module}/BACKEND-POC"
  output_path = "../${path.module}/BACKEND-POC.zip"
}

resource "aws_s3_object" "lambda_BACKEND-POC" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "BACKEND-POC.zip"
  source = data.archive_file.lambda_BACKEND-POC.output_path

  etag = filemd5(data.archive_file.lambda_BACKEND-POC.output_path)
}

