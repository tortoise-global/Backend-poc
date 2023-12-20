/*
#define variables
locals {
  layer_zip_path    = "layer.zip"
  layer_name        = "my_lambda_requirements_layer"
  //requirements_path = "${path.root}/../requirements.txt"
  requirements_path = "${path.root}/requirements.txt"

}

# create zip file from requirements.txt. Triggers only when the file is updated
resource "null_resource" "lambda_layer" {
  triggers = {
    //requirements = filesha1(local.requirements_path)
    requirements = filesha1(local.requirements_path)

  }
  # the command to install python and dependencies to the machine and zips
  provisioner "local-exec" {
    command = <<EOT
      //set -e
      sudo apt-get update
      sudo apt install python3 python3-pip zip -y
      sudo rm -rf python
      sudo mkdir python
      //sudo  pip3 install -r ${local.requirements_path} -t python/
      //zip -r ${local.layer_zip_path} python/

      sudo pip3 install -r requirements.txt -t python/
      sudo zip -r  python.zip python/
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
  depends_on = [null_resource.lambda_layers] # triggered only if the zip file is created
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
*/



/*
# Create a Python virtual environment
resource "null_resource" "lambda_layers" {
  triggers = {
    requirements = filesha1(local.requirements_path)
  }

  provisioner "local-exec" {
    command = <<EOT
      set -e
      //python3 -m venv myenv
      //source myenv/bin/activate
      apt install python3 python3-pip zip -y
      pip3 install -r ${local.requirements_path} -t 
     // deactivate
      zip -r ${local.layer_zip_path}
    EOT
  }
}





# Create Lambda Layer
resource "aws_lambda_layer_version" "my_lambda_layer" {
  filename   = "python.zip"  # Replace with the path to your ZIP file
  layer_name = "my_lambda_layer"
  
  compatible_runtimes = ["python3.11"]  # Replace with your desired Python version
}

output "layer_arn" {
  value = aws_lambda_layer_version.my_lambda_layer.arn
}



# Attach Lambda Layer to Lambda function
resource "aws_lambda_function" "BACKEND-POC" {
  function_name         = "BACKEND-POC"
  s3_bucket             = aws_s3_bucket.lambda_bucket.id
  s3_key                = aws_s3_object.lambda_BACKEND-POC.key
  runtime               = "python3.11"
  handler               = "function.lambda_handler"
  source_code_hash      = data.archive_file.lambda_BACKEND-POC.output_base64sha256
  role                  = aws_iam_role.BACKEND-POC_lambda_exec.arn

  # Attach Lambda Layer
  layers = [aws_lambda_layer_version.my_lambda_layer.arn]
}

*/

# Create Lambda Layer
resource "aws_lambda_layer_version" "my_lambda_layer" {
  filename             = "python.zip"  # Replace with the path to your ZIP file
  layer_name           = "my_lambda_layer"
  compatible_runtimes  = ["python3.11"]  # Replace with your desired Python version
}


//output "layer_arn" {
  //value = aws_lambda_layer_version.my_lambda_layer.arn
//}

