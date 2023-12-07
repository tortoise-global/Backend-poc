/*
resource "aws_s3_bucket" "tf_state_bucket" {
  bucket = "turtilbacendtf"
  acl    = "private" # ACL for the bucket, you can modify this as needed

  tags = {
    Name = "TerraformStateBucket"
  }
}
*/


provider "aws" {
  region = "ap-south-1"
}


terraform {
  backend "s3" {
    bucket = aws_s3_bucket.tf_state_bucket.id
    key    = "turtlebackend.tfstate"
    region = "ap-south-1"
  }
}







