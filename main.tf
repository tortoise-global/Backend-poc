/*
resource "aws_s3_bucket" "tf_state_bucket" {
  bucket = "turtilbacendtf"
  acl    = "private" # ACL for the bucket, you can modify this as needed

  tags = {
    Name = "TerraformStateBucket"
  }
}



terraform {
  backend "s3" {
    bucket = turtilbacendtf
    key    = "turtlebackend.tfstate"
    region = "ap-south-1"
  }
}

provider "aws" {
  region = "ap-south-1"
}



module "vpc-infra" {
  source = "./modules/vpc"

  # VPC Input Vars
  vpc_cidr             = local.vpc_cidr
  availability_zones   = local.availability_zones
  public_subnet_cidrs  = local.public_subnet_cidrs
  private_subnet_cidrs = local.private_subnet_cidrs
}


module "tf-state" {
  source      = "./modules/tf-state"
  bucket_name = "tf-state-backend-ci-cd"
}
*/


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
  region = "ap-south-1"
}













