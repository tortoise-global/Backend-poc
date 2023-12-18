#define variables
locals {
  layer_zip_path    = "layer.zip"
  layer_name        = "my_lambda_requirements_layer"
  //requirements_path = "${path.root}/../requirements.txt"
  requirements_path = "requirements.txt"

}
/*
# create zip file from requirements.txt. Triggers only when the file is updated
resource "null_resource" "lambda_layer" {
  triggers = {
    //requirements = filesha1(local.requirements_path)
    requirements = filesha1(local.requirements_path)

  }
  # the command to install python and dependencies to the machine and zips
  provisioner "local-exec" {
    command = <<EOT
      set -e
      apt-get update
      apt install python3 python3-pip zip -y
      rm -rf python
      mkdir python
      pip3 install -r ${local.requirements_path} -t python/
      zip -r ${local.layer_zip_path} python/
    EOT
  }
}
*/

# Create a Python virtual environment
resource "null_resource" "lambda_layer" {
  triggers = {
    requirements = filesha1(local.requirements_path)
  }

  provisioner "local-exec" {
    command = <<EOT
      set -e
      //python3 -m venv myenv
      //source myenv/bin/activate
      pip3 install -r ${local.requirements_path} -t myenv/lib/python3.11/site-packages/
     // deactivate
      zip -r ${local.layer_zip_path} myenv/lib/python3.11/site-packages/
    EOT
  }
}

# define existing bucket for storing lambda layers
resource "aws_s3_bucket" "lambda_layer_bucket" {
  bucket = "my-lambda-layer-buckets"
}

# upload zip file to s3
resource "aws_s3_object" "lambda_layer_zip" {
  bucket     = aws_s3_bucket.lambda_layer_bucket.id
  key        = "lambda_layers/${local.layer_name}/${local.layer_zip_path}"
  source     = local.layer_zip_path
  depends_on = [null_resource.lambda_layer] # triggered only if the zip file is created
}

# create lambda layer from s3 object
resource "aws_lambda_layer_version" "my-lambda-layer" {
  s3_bucket           = aws_s3_bucket.lambda_layer_bucket.id
  s3_key              = aws_s3_object.lambda_layer_zip.key
  layer_name          = local.layer_name
  compatible_runtimes = ["python3.11"]
  skip_destroy        = true
  depends_on          = [aws_s3_object.lambda_layer_zip] # triggered only if the zip file is uploaded to the bucket
}