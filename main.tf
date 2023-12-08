

terraform {
  # Run init/plan/apply with "backend" commented-out (ueses local backend) to provision Resources (Bucket, Table)
  # Then uncomment "backend" and run init, apply after Resources have been created (uses AWS)
  backend "s3" {
    bucket         = "tf-state-backend-ci-cd"
    key            = "tf-infra/terraform.tfstate"
    region         = "ap-south-1"
    //dynamodb_table = "terraform-state-locking"
    //encrypt        = true
  }

}


provider "aws" {
  region = "us-east-1"
}













