terraform {
  backend "s3" {
    bucket = "turtilbacendtf"
    key    = "turtlebackend.tfstate"
    region = "ap-south-1"
  }
}


provider "aws" {
  region = "ap-south-1"
}






