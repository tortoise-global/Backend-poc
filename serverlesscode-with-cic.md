# Running Terraform via AWS Developer Tools — Complete CI/CD 


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

provider "aws" {
  region = "us-east-1"
}

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

## s3variables.tf

```
variable "bucket_name" {
  description = "Remote S3 Bucket Name"
  default =  "tf-state-backend-ci-cd" // change name i.e  "tf-state-backend-ci-cd" with your own bucketname
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
  default =  "tf-state-backend-ci-cd"  // change name i.e  "tf-state-backend-ci-cd" with your own bucketname
  validation {
    condition     = can(regex("^([a-z0-9]{1}[a-z0-9-]{1,61}[a-z0-9]{1})$", var.bucket_name))
    error_message = "Bucket Name must not be empty and must follow S3 naming rules."
  }
}

```

## Defines the variables used in the Terraform configuration:

run the below commands in your local terminal or commandprompt when we run Terraform commands i.e Terraform init, Terraform apply.

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


### Step 1: Provisioning CodeCommit Repository
CodeCommit Repository will be used to store the Terraform code, which we will be using to provision the other resources except whatever mentioned earlier. Let's say you want to set up a complex VPC architecture. This approach will show you how to create a CI/CD pipeline to run that Terraform inside CodeBuild to provision that VPC.

Create one workspace folder in your system & put the below mentioned code files inside that. Definitely change the parameters as per your needs.


## provider.tf


```
provider "aws" {
  region = var.aws_region
}

```


## variables.tf


```
variable "aws_region" {
  type = string
  default = "us-east-1"
}

variable "codecommit_repository_name" {
  type = string
  default = "infra-vpc-repo"
}

```


## main.tf

# NOTE   bucket = "tf-state-backend-ci-cd". tf-state-backend-ci-cd bucket is created starting

```

terraform {
  # Run init/plan/apply with "backend" commented-out (ueses local backend) to provision Resources (Bucket, Table)
  # Then uncomment "backend" and run init, apply after Resources have been created (uses AWS)
  backend "s3" {
    bucket = "tf-state-backend-ci-cd" // GIVE YOUR OWN CREATED BUCKET NAME IN TERRAFROM OR AWS CONSOLE
    key    = "tf-infra/terraform.tfstate"
    region = "us-east-1"
   
  }

}



resource "aws_codecommit_repository" "infra-vpc-codecommit-repo" {
  repository_name = var.codecommit_repository_name
  description = "CodeCommit Repository to store VPC infra terraform codes."
}

```

# Note: I'm using an AWS IAM account with “AdministratorAccess” to authenticate terraform via local system aws cli.First run “terraform init” & then “terraform apply” to provision the codecommit repository.

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


<img width="1440" alt="Screenshot 2023-12-26 at 7 22 52 PM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yCI5CC90tu0kDgUyxg_7lw.png">

Now go to AWS account and check CodeCommit.

<img width="1440" alt="Screenshot 2023-12-26 at 7 22 52 PM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*eyKi6xz1qsMggJ5i70eEzA.png">


### Step 2: Setting up required IAM Roles
Again, I'm going to use Terraform Code to create two IAM roles —

First one is for CodeBuild Project which is going to look at the S3 bucket to fetch the terraform state file. Also, we need to provide certain power to CodeBuild project so that it can provision resources — let's say in our case VPC.

Second one is for Pipeline in CodePipeline which is going to run the CodeBuild project. Also, we will provide permission to fetch the codes from CodeCommit.


# First, for the best practices I'm adding some more variables in “variables.tf” file.


## variables.tf


```
variable "codebuild_role_name" {
    type = string
    default = "infra-vpc-codebuild-role" 
}

variable "codepipeline_role_name" {
    type = string
    default = "infra-vpc-codepipeline-role"
}

variable "codebuild_policy_name" {
    type = string
    default = "infra-vpc-codebuild-policy" 
}

variable "codepipeline_policy_name" {
    type = string
    default = "infra-vpc-codepipeline-policy"
}



//dev variable for code build
variable "dev_codebuild_plan_project_name" {
    type = string
    default = "dev-infra-vpc-codebuild-project-plan" 
}

variable "dev_codebuild_project_test_name" {
    type = string
    default = "dev-infra-vpc-codebuild-project-project-tests" 
}

variable "dev_codebuild_apply_project_name" {
    type = string
    default = "dev-infra-vpccodebuild-project-apply" 
}


variable "dev_codepipeline_name" {
    type = string
    default = "dev-infra-vpc-codepipeline" 
}


//prod variable for code build
variable "prod_codebuild_plan_project_name" {
    type = string
    default = "prod-infra-vpc-codebuild-project-plan" 
}

variable "prod_codebuild_project_test_name" {
    type = string
    default = "prod-infra-vpc-codebuild-project-tests" 
}

variable "prod_codebuild_apply_project_name" {
    type = string
    default = "prod-infra-vpc-codebuild-project-apply" 
}

variable "prod_codepipeline_name" {
    type = string
    default = "prod-infra-vpc-codepipeline" 
}



```

# Next, we have the code to create the IAM Role for CodeBuild…


## codebuild-iam.tf


```
data "aws_iam_policy_document" "codebuild-policy-document" {
    statement{
        actions = ["logs:*"]
        resources = ["*"]
        effect = "Allow"
    }
    statement{
        actions = ["s3:*"]
        resources = ["*"]
        effect = "Allow"
    }

  statement {
        actions = ["iam:*"]
        resources = ["*"]
        effect = "Allow"
    }

  statement {
        actions = ["lambda:*"]
        resources = ["*"]
        effect = "Allow"
    }
 

  statement {
        actions = ["apigateway:*"]
        resources = [ 
          "*"
          ]
        effect = "Allow"
    }


  statement {
        actions = ["codecommit:*"]
        //resources = ["arn:aws:codecommit:us-east-1:033464272864:turtil-repo"]
        resources = ["*"]

        effect = "Allow"
    }
  
  statement {
    actions   = ["codepipeline:*"]  // Add the missing CodePipeline action
    resources = ["*"]  // Update resource ARN to match your CodePipeline

    effect    = "Allow"
  }

  statement {
    actions   = ["codebuild:*"]  // Add the missing CodeBuild action
    resources = ["*"]  // Update resource ARNs if necessary
    effect    = "Allow"
  }

  statement {
    actions   = ["dynamodb:*"]
    resources = ["*"]
    effect    =  "Allow"
  }

  statement {
    actions   = ["route53:*"]
    resources = ["*"]
    effect    =  "Allow"
  }

  statement {
    actions   = ["acm:*"]
    resources = ["*"]
    effect    =  "Allow"
  }

  statement {
    actions   = ["git:*"]
    resources = ["*"]
    effect    =  "Allow"
  }

}

resource "aws_iam_policy" "codebuild-policy" {
    name = var.codebuild_policy_name
    path = "/"
    policy = data.aws_iam_policy_document.codebuild-policy-document.json
}

resource "aws_iam_role" "codebuild-role" {
  name = var.codebuild_role_name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


resource "aws_iam_role_policy_attachment" "codebuild-policy-attachment1" {
    policy_arn  = aws_iam_policy.codebuild-policy.arn
    role        = aws_iam_role.codebuild-role.id
}

resource "aws_iam_role_policy_attachment" "codebuild-policy-attachment2" {
    policy_arn  = "arn:aws:iam::aws:policy/AmazonVPCFullAccess"
    role        = aws_iam_role.codebuild-role.id
}


```

We are creating one IAM role for CodeBuild project which has permissions on VPC, inside of our specified S3 bucket & on CloudWatch Logs. Simply because CodeBuild Project going to provision VPC for us using Terraform & it will maintain the Terraform state file in S3. Also, it will store the execution logs in CloudWatch Logs.

Run “terraform apply” & check the logs. Also, check on AWS console…

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


<img width="1440" alt="Screenshot 2023-12-26 at 7 22 52 PM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_enUOgo5zjpdsobCd3mQMg.png">



<img width="1440" alt="Screenshot 2023-12-26 at 7 22 52 PM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*bGtkswLm3CKkP2Jmhu8fWw.png">

# Next, we will be creating another code for setting up IAM role for CodePipeline…


## codepipeline-iam.tf


```
data "aws_caller_identity" "current" {}

locals {
    account_id = data.aws_caller_identity.current.account_id
}

data "aws_iam_policy_document" "codepipeline-policy-document" {
    statement{
        actions = ["cloudwatch:*"]
        resources = ["*"]
        effect = "Allow"
    }
    statement{
        actions = ["codebuild:*"]
        resources = [
          "*"

          ]
        effect = "Allow"
    }
    statement{
        actions = ["codecommit:*"]
        resources = [aws_codecommit_repository.infra-vpc-codecommit-repo.arn]
        //resources = ["*"]
        effect = "Allow"
    }

   

    statement{
        actions = ["s3:*"]
        resources = [ 
            //"${aws_s3_bucket.s3-bucket-backend.arn}/*"
            //"arn:aws:s3:::cicd-s3-backend/*"
            "*"
            ]
        effect = "Allow"
    }
}

resource "aws_iam_policy" "codepipeline-policy" {
    name = var.codepipeline_policy_name
    path = "/"
    policy = data.aws_iam_policy_document.codepipeline-policy-document.json
}

resource "aws_iam_role" "codepipeline-role" {
  name = var.codepipeline_role_name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "codepipeline.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

}


resource "aws_iam_role_policy_attachment" "codepipeline-policy-attachment" {
    policy_arn  = aws_iam_policy.codepipeline-policy.arn
    role        = aws_iam_role.codepipeline-role.id
}



```


This role has the specific permissions to fetch the terraform code from CodeCommit. Next it can run our own created CodeBuild project. Also, it can store the artifact in S3 inside our specified bucket. We are giving CloudWatch permission so that in future CodePipeline can be integrated with CloudWatch events.

# The reason we are creating one local variable called “account_id” is that still we haven't created CodeBuild projects, so terraform can't access it's ARN. Hence, we created the ARN manually using the project name from variables file & the account id.

# Run the terraform command & check IAM in AWS…


<img width="1440" alt="Screenshot 2023-12-26 at 7 22 52 PM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*01i9REfRwIgbdYuC18tUDw.png">


<img width="1440" alt="Screenshot 2023-12-26 at 7 22 52 PM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*L3VIVRTenXI1iGaIy5aNGw.png">


### Step 3: Provisioning CodeBuild Project
Finally, it's time to create the CodeBuild project. First look at the below code & after that I'm explaining how it's working.


## codebuild.tf


```
resource "aws_codebuild_project" "dev_codebuild_project_plan_stage" {
  name          = var.dev_codebuild_plan_project_name
  description   = "Terraform Planning Stage for turtil"
  service_role  = aws_iam_role.codebuild-role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "hashicorp/terraform:latest"
    type                        = "LINUX_CONTAINER"

    environment_variable {
      name  = "ENVINORMENT_VARIABLE"
      value = "dev"
    }
 }
 
  source {
     type   = "CODEPIPELINE"
     buildspec = file("buildspec/plan-buildspec.yml")
 }
}


resource "aws_codebuild_project" "dev_codebuild_project_test_stage" {
  name          = var.dev_codebuild_project_test_name
  description   = "Test Planning Stage for turtil"
  service_role  = aws_iam_role.codebuild-role.arn

  artifacts {
    type = "CODEPIPELINE"
  }


  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:5.0" # Choose the appropriate Docker image
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD" # Use CODEBUILD or SERVICE_ROLE depending on your setup
  }
 
 
  source {
     type   = "CODEPIPELINE"
     buildspec = file("buildspec/test-buildspec.yml")
 }
}




resource "aws_codebuild_project" "dev_codebuild_project_apply_stage" {
  name          = var.dev_codebuild_apply_project_name
  description   = "Terraform Apply Stage for turtil"
  service_role  = aws_iam_role.codebuild-role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "hashicorp/terraform:latest"
    type                        = "LINUX_CONTAINER"

    environment_variable {
      name  = "ENVINORMENT_VARIABLE"
      value = "dev"
    }
 }

  source {
     type   = "CODEPIPELINE"
     buildspec = file("buildspec/apply-buildspec.yml")
 }
}


resource "aws_codebuild_project" "prod_codebuild_project_plan_stage" {
  name          = var.prod_codebuild_plan_project_name
  description   = "Terraform Planning Stage for turtil"
  service_role  = aws_iam_role.codebuild-role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "hashicorp/terraform:latest"
    type                        = "LINUX_CONTAINER"

    environment_variable {
      name  = "ENVINORMENT_VARIABLE"
      value = "prod"
    }
 }
 
  source {
     type   = "CODEPIPELINE"
     buildspec = file("buildspec/plan-buildspec.yml")
 }
}


resource "aws_codebuild_project" "prod_codebuild_project_test_stage" {
  name          = var.prod_codebuild_project_test_name
  description   = "Test Planning Stage for turtil"
  service_role  = aws_iam_role.codebuild-role.arn

  artifacts {
    type = "CODEPIPELINE"
  }


  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:5.0" # Choose the appropriate Docker image
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD" # Use CODEBUILD or SERVICE_ROLE depending on your setup
  }
 
 
  source {
     type   = "CODEPIPELINE"
     buildspec = file("buildspec/test-buildspec.yml")
 }
}




resource "aws_codebuild_project" "prod_codebuild_project_apply_stage" {
  name          = var.prod_codebuild_apply_project_name
  description   = "Terraform Apply Stage for turtil"
  service_role  = aws_iam_role.codebuild-role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "hashicorp/terraform:latest"
    type                        = "LINUX_CONTAINER"

    environment_variable {
      name  = "ENVINORMENT_VARIABLE"
      value = "prod"
    }
 }

  source {
     type   = "CODEPIPELINE"
     buildspec = file("buildspec/apply-buildspec.yml")
 }
}


```


Here we are simply creating two CodeBuild projects — one is to run “terraform plan” command & another is to run “terraform apply” command, so that if plan command fail, we don't run the apply command later on.

Also, we can see that CodeBuild source & artifact is managed by CodePipeline. Now when we will invoke CodeBuild, we’re going to run some terraform command inside the container & for that we are using “hashicorp/terraform:latest” container image.

### NOTE YOU CAN CREATE BUILD FILES IN CODEBUILD OR BY FOLLOWING BELOW STEPS

Now we are going to write those terraform commands which we want to run inside containers. So, in your workspace create one folder called “buildspec” & put the below mentioned three files…

<img width="215" alt="Screenshot 2024-03-06 at 10 55 35 PM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/df863292-a1ad-4ff1-9762-b145788d4635">

# plan-buildspec.yml

```
version: 0.2
phases:
  pre_build:
    commands:
      - cd my-terraform-files
      - terraform init
      
      - terraform workspace select ${ENVINORMENT_VARIABLE}

      - terraform validate 
 
  build:
    commands:
      - terraform plan 
    
```

# apply-buildspec.yml

```

version: 0.2
phases:
  pre_build:
    commands:
      - cd my-terraform-files
      - terraform init
     
      - terraform workspace select ${ENVINORMENT_VARIABLE}
     
      - terraform validate
      
 
  build:
    commands:
      - terraform apply --auto-approve
    
```
### Note create a folder tests then only test-buildspec.yml work

<img width="208" alt="Screenshot 2024-03-06 at 11 07 19 PM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/aaf531c3-1ec3-4522-b43a-dc54ea094376">




# test-buildspec.yml

```
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.7
  build:
    commands:
      - python -m unittest discover tests
artifacts:
  files:
    - '**/*'
```

# We are done. Let's run the terraform command again & check on AWS Console.

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

<img width="208" alt="Screenshot 2024-03-06 at 11 07 19 PM" src="https://miro.medium.com/v2/resize:fit:4800/format:webp/1*LnwGnLTB3jK3HrTsQqEEog.png">

<img width="208" alt="Screenshot 2024-03-06 at 11 07 19 PM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*r3UQ9ocD_ZdFN5cKtzKSxg.png">


# Step 4: Provisioning CodePipeline Project

We are very close to complete our whole setup. This is the last file we going to create to complete this whole CI/CD setup. See the below code.

## codepipeline.tf

# Note give s3 bucket name in our case i.e tf-state-backend-ci-cd  in artifact_store {location = "tf-state-backend-ci-cd"}

```

resource "aws_codepipeline" "prod_codepipeline" {

    name = var.prod_codepipeline_name
    role_arn = aws_iam_role.codepipeline-role.arn

    artifact_store {
        type="S3"
        //location = aws_s3_bucket.cicd-s3-backend.bucket
        //location = "s3-terraform-backend-and-artifact"
        location = "tf-state-backend-ci-cd"


    }

    stage {
        name = "Source"
        action{
            name = "Source"
            category = "Source"
            owner = "AWS"
            provider = "CodeCommit"
            version = "1"
            output_artifacts = ["infra_vpc_code"]
            configuration = {
                RepositoryName = aws_codecommit_repository.infra-vpc-codecommit-repo.repository_name
                BranchName   = "main"
                OutputArtifactFormat = "CODE_ZIP"
            }
        }
    }

    stage {
        name ="Plan"
        action{
            name = "Build"
            category = "Build"
            provider = "CodeBuild"
            version = "1"
            owner = "AWS"
            input_artifacts = ["infra_vpc_code"]
            configuration = {
                ProjectName = aws_codebuild_project.prod_codebuild_project_plan_stage.name
            }
        }
    }

    stage {
        name ="Test"
        action{
            name = "Build"
            category = "Build"
            provider = "CodeBuild"
            version = "1"
            owner = "AWS"
            input_artifacts = ["infra_vpc_code"]
            configuration = {
                ProjectName = aws_codebuild_project.prod_codebuild_project_test_stage.name
            }
        }
    }

    

    stage {
        name ="Deploy"
        action{
            name = "Deploy"
            category = "Build"
            provider = "CodeBuild"
            version = "1"
            owner = "AWS"
            input_artifacts = ["infra_vpc_code"]
            configuration = {
                ProjectName = aws_codebuild_project.prod_codebuild_project_apply_stage.name
            }
        }
    }

}



resource "aws_codepipeline" "dev_codepipeline" {

    name = var.dev_codepipeline_name
    role_arn = aws_iam_role.codepipeline-role.arn

    artifact_store {
        type="S3"
        //location = aws_s3_bucket.cicd-s3-backend.bucket
        location = "s3-terraform-backend-and-artifact"

    }

    stage {
        name = "Source"
        action{
            name = "Source"
            category = "Source"
            owner = "AWS"
            provider = "CodeCommit"
            version = "1"
            output_artifacts = ["dev_infra_vpc_code"]
            configuration = {
                RepositoryName = aws_codecommit_repository.infra-vpc-codecommit-repo.repository_name
                BranchName   = "dev"
                OutputArtifactFormat = "CODE_ZIP"
            }
        }
    }

    stage {
        name ="Plan"
        action{
            name = "Build"
            category = "Build"
            provider = "CodeBuild"
            version = "1"
            owner = "AWS"
            input_artifacts = ["dev_infra_vpc_code"]
            configuration = {
                ProjectName = aws_codebuild_project.dev_codebuild_project_plan_stage.name
            }
        }
    }

    stage {
        name ="Test"
        action{
            name = "Build"
            category = "Build"
            provider = "CodeBuild"
            version = "1"
            owner = "AWS"
            input_artifacts = ["dev_infra_vpc_code"]
            configuration = {
                ProjectName = aws_codebuild_project.dev_codebuild_project_test_stage.name
            }
        }
    }

    

    stage {
        name ="Deploy"
        action{
            name = "Deploy"
            category = "Build"
            provider = "CodeBuild"
            version = "1"
            owner = "AWS"
            input_artifacts = ["dev_infra_vpc_code"]
            configuration = {
                ProjectName = aws_codebuild_project.dev_codebuild_project_apply_stage.name
            }
        }
    }

}




```


Little bit bigger code, but easy to understand. We are creating one Pipeline in CodePipeline which has three stages. Now it's a constraint in CodePipeline that you have to provide one S3 bucket name where CodePipeline will store its artifacts. Simply because each of the CodePipeline Stages run in an independent container & if you pull code in 1st stage & then in 2nd stage if you want to use that code, then that can be achieved only if CodePipeline stores the code in some centralized location. Currently that location is S3 for CodePipeline.

This is the reason we can notice whatever output artifacts CodePipeline is generating, is exactly same what we are passing as input artifacts in second & third stage.

Next, in Plan & Deploy stage we are running those 6 CodeBuild Projects we created earlier.

# Let's run terraform apply for the last time…

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

<img width="208" alt="Screenshot 2024-03-06 at 11 07 19 PM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KlHCLzhiQGsJmT3KDA7TjQ.png">


# Hold on… You might see that your CodePipeline failed, simply because It's picking up the codes from CodeCommit repository, but still we haven't created any code there.

<img width="208" alt="Screenshot 2024-03-06 at 11 07 19 PM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*eebwGjZdkUshm9UQY--E9A.png">


# Step 4: Configure git for  Cloning CodeCommit Repository

### If you know Git & GitHub, then let me tell you when you create one Repository in GitHub without initializing then it's like a blank folder, which still haven't been git initialized. Now there's two techniques…

### First, you can create a local system folder.Use git to initialize that folder. Put your codes. Setup the remote location to upload the code in remote repository. Then finally do the “git push”.

### Second one is much simpler. Initialize your remote repository with a “README.md” file. Then clone that repository in local system. Put your codes & then upload the code.

### Third, you can clone  the repository and upload the code in remote repository. Then finally do the “git push”.


### I'm choosing the Third method, so let's go to CodeCommit & clone  the repository.

### Before starting the second method we need to configure git for codecommit

# step-1 follow the image below 

<img width="1440" alt="Screenshot 2024-03-07 at 8 09 20 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/82be05fc-929e-40b5-b7f5-562846cd64b7">


# step-2  click on https git  generate credentials

<img width="1440" alt="Screenshot 2024-03-07 at 8 09 44 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/5b218d34-19bf-4bae-aba5-ae30eb43220f">

# step-3 download the generate credentials or copy them somewhere

<img width="1440" alt="Screenshot 2024-03-07 at 8 10 30 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/a38561a2-45f8-47b4-a8af-bfdbfb1c5e47">




### Now there's various methods available to clone the CodeCommit repository in your local system but remember one thing that AWS root account can't clone the repository. Initially I told you that I'm using an AWS IAM account which has “AdministratorAccess”. I used that account access key & secret key to configure AWS CLI on my local system. Hence, I'm able to run the Terraform commands.

### You can use that same AWS account to clone the repository & for that on your local system install “Python3” & run the below command to install “git-remote-codecommit” library.

### run the below command to install “git-remote-codecommit” library.
```
pip3 install git-remote-codecommit

```

<img width="1440" alt="Screenshot 2024-03-07 at 8 10 30 AM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*xaxEBy-BK_gDzH4kpdZ1WA.png">


### Now if you have your AWS CLI configured the go to AWS CodeCommit repository & copy the “HTTPS (GRC)” URL.

### Reference Document: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-git-remote-codecommit.html

### Finally run the git clone command & hopefully you will be able to clone the repository.

<img width="1440" alt="Screenshot 2024-03-07 at 8 10 30 AM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yChiO6jTHyvVOSkZCGEIpg.png">


###  it will ask you username and password copy and paste the username password which we download from this below image



<img width="1440" alt="Screenshot 2024-03-07 at 8 10 30 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/a38561a2-45f8-47b4-a8af-bfdbfb1c5e47">




<img width="1440" alt="Screenshot 2024-03-07 at 8 10 30 AM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*J7n7shEc4dTfwnw4rVdHNg.png">


# Step 5: Configure code structure as per codepipeline and codebuild requirments

### step1 : the code  should have folder name with my-terraform-files in that folder create a terroform files with any file names

### as shown in picture below

<img width="1440" alt="Screenshot 2024-03-07 at 9 10 23 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/b788e9bf-a898-4dbf-a1eb-cb3f1b3e48ab">


### step2 : the code  should have folder name with tests in that folder create a test cases for apis with any file names

### as shown in picture below

<img width="1440" alt="Screenshot 2024-03-07 at 9 20 39 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/5f6a31d4-8cad-46aa-86f6-cba08732e259">


### the code structure should be like this as shown in picture below 

<img width="200" alt="Screenshot 2024-03-07 at 9 25 44 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/aa23cb0c-1603-41b1-b84f-090e37cb32bb">


# Step 6: how to setup dev envirnorment and prod envirorment for a python project

### clone a repository from the code commit

<img width="200" alt="Screenshot 2024-03-07 at 9 25 44 AM" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*J7n7shEc4dTfwnw4rVdHNg.png">

### step1 : the code  should have folder name with my-terraform-files in that folder create a terroform files with any file names

### as shown in picture below

<img width="1440" alt="Screenshot 2024-03-07 at 9 10 23 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/b788e9bf-a898-4dbf-a1eb-cb3f1b3e48ab">


### step2 : the code  should have folder name with tests in that folder create a test cases for apis with any file names

### as shown in picture below

<img width="1440" alt="Screenshot 2024-03-07 at 9 20 39 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/5f6a31d4-8cad-46aa-86f6-cba08732e259">


### the code structure should be like this as shown in picture below 

<img width="200" alt="Screenshot 2024-03-07 at 9 25 44 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/aa23cb0c-1603-41b1-b84f-090e37cb32bb">

### create all-folders and files as shown in below

<img width="191" alt="Screenshot 2024-03-07 at 9 48 09 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/1f256de6-2e03-4506-a83f-8bb21dd7c100">

### create a folders and  files in folder lambdas as shown in above

### folder demo_lambda has 2 files config.py, lambda_fun.py

### config.py

```

def my_config(endpoint, url):
        
        dev = "/v1/dev"+endpoint

        prod = "/v2/prod"+endpoint


        if endpoint == '/add_post' or endpoint == '/allpost':

            if url in dev:
                table_name = 'dev_cicdpost'
                return table_name

            if url in prod:
                table_name = 'prod_cicdpost'
                return table_name
            return table_name

```

### lambda_fun.py

```
import json
import boto3
from config import my_config



def lambda_handler(event, context):

   
    body = None
    token = None
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }

    
    if 'httpMethod' in event and 'resource' in event:
    # if 1:
        http_method, route = event['httpMethod'], event['resource']

        
        #create post
        if http_method == 'POST' and route == '/add_post':

            host = event.get('path', None)
            print("path", host)
            
            table_name = my_config(route, host)

            dynamodb = boto3.resource('dynamodb')
            
            table = dynamodb.Table(table_name)
            request_json = json.loads(event['body'])
            table.put_item(
                Item=request_json
            )
            body = request_json
            body = json.dumps(body)
            return {
                'statusCode': status_code,
                'body': body,
                'headers': headers
            }


```



### folder demo2_lambda has 2 files config.py, lambda_fun2.py

### config.py

```
def my_config(endpoint, url):
        
        dev = "/v1/dev"+endpoint

        prod = "/v2/prod"+endpoint



        if endpoint == '/add_comment' or endpoint == '/allcomment':
             
            if url in dev:
                table_name = 'dev_cicdcomment'
                return table_name


            if url in prod:
                table_name = 'prod_cicdcomment'
                return table_name

            return table_name
```

### lambda_fun2.py

```
import json
import boto3

from config import my_config





def lambda_handler(event, context):
    body = None
    token = None
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }

    
    if 1:
        http_method, route = event['httpMethod'], event['resource']

        
       
        if http_method == 'POST' and route == '/add_comment':

            host = event.get('path', None)
            print("path", host)
            
            table_name = my_config(route, host)

            dynamodb = boto3.resource('dynamodb')
            
            table = dynamodb.Table(table_name)
            request_json = json.loads(event['body'])
            table.put_item(
                Item=request_json
            )
            body = request_json
            body = json.dumps(body)
            return {
                'statusCode': status_code,
                'body': body,
                'headers': headers
            }
        

```



### Setting up the Terraform Backend to use S3 bucket

### go to my-terraform-files folder in there create main.tf

Now let's start the coding for the VPC development. But before that I will request you go to your S3 bucket & check inside “terraform_backend” folder. It will be empty.

First, we’re going to setup the “backend” for terraform & the provider as well. Because these terraform files going to run in CodeCommit & it needs to fetch the state file from a centralized location.

### main.tf
```
terraform {
  # Run init/plan/apply with "backend" commented-out (ueses local backend) to provision Resources (Bucket, Table)
  # Then uncomment "backend" and run init, apply after Resources have been created (uses AWS)
  backend "s3" {
    bucket = "s3-backend-for-turtil-repo-test" // s3-bucket can be created  in aws console or your can check Terraform S3 Bucket Configuration starting of the doc
    key    = "tf-infra/terraform.tfstate"
    region = "us-east-1"
  }

}


provider "aws" {
  region = "us-east-2"
}

```

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

### go to my-terraform-files folder in there create variables.tf

```
// ####### define lambda data ############

/*
variable "environment" {
  //description = "The environment in which resources should be provisioned"
  //default     = "development"
}


variable "api_stage_name" {
  //description = "The name of the API Gateway stage"
  //type        = string
  //default     = "dev"
}

*/

variable "lambda_im_policy" {
  //type    = string
  //default = "CICDS2-TURTIL-APP-lambda"

  type = map(string)

  default = {
    "dev" = "CICDS2-TURTIL-APP-lambda"
    "prod" = "PROD-CICDS2-TURTIL-APP-lambda"
  }
}


variable "dynamodb_policy_name" {
  //type    = string
  //default = "CICDS2TurtilDynamoDBPolicy"

  type = map(string)

  default = {
    "dev" = "CICDS2TurtilDynamoDBPolicy"
    "prod" = "PRODCICDS2TurtilDynamoDBPolicy"
  }
}


variable "lambda_function_name" {
  //type    = string
  //default = "CICDS2-TURTIL-APP"

  type = map(string)

  default = {
    "dev" = "CICDS2-TURTIL-APP"
    "prod" = "PROD-CICDS2-TURTIL-APP"
  }
}

variable "lambda_runtime" {
  //type    = string
  //default = "python3.11"
  type = map(string)

  default = {
    "dev" = "python3.11"
    "prod" = "python3.11"
  }
}

variable "lambda_handler" {
  //type    = string
  //default = "lambda_fun.lambda_handler"

  type = map(string)

  default = {
    "dev" = "lambda_fun.lambda_handler"
    "prod" = "lambda_fun.lambda_handler"
  }
}

variable "lambda_timeout" {
  //type    = number
  //default = 600

  type = map(number)

  default = {
    "dev" = 600
    "prod" = 600
  }
}

variable "lambda_cloudwatch_log_retention" {
  //type    = number
  //default = 14

  type = map(number)

  default = {
    "dev" = 14
    "prod" = 14
  }
}


variable "lambda_s3_key" {
  //type    = string
  //default = "CICDS2-TURTIL-APP.zip"

  type = map(string)

  default = {
    "dev" = "CICDS2-TURTIL-APP.zip"
    "prod" = "PRODCICDS2-TURTIL-APP.zip"
  }
}


// 2nd lambda 


variable "lambda_function_name2" {
  //type    = string
  //default = "CICDS2-TURTIL-APP"

  type = map(string)

  default = {
    "dev" = "CICDS2-TURTIL-APP2"
    "prod" = "PROD-CICDS2-TURTIL-APP2"
  }
}

variable "lambda_runtime2" {
  //type    = string
  //default = "python3.11"
  type = map(string)

  default = {
    "dev" = "python3.11"
    "prod" = "python3.11"
  }
}

variable "lambda_handler2" {
  //type    = string
  //default = "lambda_fun2.lambda_handler"

  type = map(string)

  default = {
    "dev" = "lambda_fun2.lambda_handler"
    "prod" = "lambda_fun2.lambda_handler"
  }
}



variable "lambda_timeout2" {
  //type    = number
  //default = 600

  type = map(number)

  default = {
    "dev" = 600
    "prod" = 600
  }
}

variable "lambda_cloudwatch_log_retention2" {
  //type    = number
  //default = 14

  type = map(number)

  default = {
    "dev" = 14
    "prod" = 14
  }
}


variable "lambda_s3_key2" {
  //type    = string
  //default = "CICDS2-TURTIL-APP.zip"

  type = map(string)

  default = {
    "dev" = "CICDS2-TURTIL-APP2.zip"
    "prod" = "PRODCICDS2-TURTIL-APP2.zip"
  }
}


// ######### define apigateway data #######

variable "api_name" {
  //description = "The name of the API Gateway"
  //default     = "cicd-main"

  type = map(string)

  default = {
    "dev" = "cicd-main"
    "prod" = "PROD-cicd-main"
  }
}

variable "stage_name" {
  //description = "The name of the API Gateway stage"
  //default     = "dev"

  type = map(string)

  default = {
    "dev" = "dev"
    "prod" = "PROD"
  }
}

variable "log_retention_days" {
 //description = "The number of days to retain logs in CloudWatch"
 //default     = 14

 type = map(number)

  default = {
    "dev" = 14
    "prod" = 14
  }
}



// ########### custom domain data ######################################

# Define variables
variable "domain_name" {
  //description = "The domain name for the TLS certificate and API Gateway domain"
  //type        = string
  //default     = "devcicd.turtil.co"

  type = map(string)

  default = {
    "dev" = "devcicd.turtil.co"
    "prod" = "cicd.turtil.co"
  }
}

variable "route53_zone_name" {
  //description = "The name of the Route53 hosted zone"
  //type        = string
  //default     = "turtil.co"

  type = map(string)

  default = {
    "dev" = "turtil.co"
    "prod" = "turtil.co"
  }
}

variable "validation_method" {
  //description = "The validation method for the TLS certificate"
  //type        = string
  //default     = "DNS"

  type = map(string)

  default = {
    "dev" = "DNS"
    "prod" = "DNS"
  }
}

variable "route53_ttl" {
  //description = "The TTL for the Route53 record"
  //type        = number
  //default     = 60

  type = map(number)

  default = {
    "dev" = 60
    "prod" = 60
  }
}

variable "endpoint_type" {
  //description = "The type of endpoint for the API Gateway domain"
  //type        = string
  //default     = "REGIONAL"

  type = map(string)

  default = {
    "dev" = "REGIONAL"
    "prod" = "REGIONAL"
  }
}

variable "security_policy" {
  //description = "The security policy for the API Gateway domain"
  //type        = string
  //default     = "TLS_1_2"

  type = map(string)

  default = {
    "dev" = "TLS_1_2"
    "prod" = "TLS_1_2"
  }
}

variable "api_mapping_key" {
  //description = "The API mapping key for a specific version"
  //type        = string
  //default     = "v1"

  type = map(string)

  default = {
    "dev" = "v1/dev"
    "prod" = "v2/prod"
  }
}







//dynamodb table names for dev and prod

variable "cicdpost_table_name" {
  description = "Name of the cicddemo DynamoDB table"

  type = map(string)

  default = {
    "dev" = "dev_cicdpost"
    "prod" = "prod_cicdpost"
  }
  
}


variable "cicdcomment_table_name" {
  description = "Name of the cicddemo DynamoDB table"

  type = map(string)

  default = {
    "dev" = "dev_cicdcomment"
    "prod" = "prod_cicdcomment"
  }
  
}


```

### dynmodb.tf

```

resource "aws_dynamodb_table" "cicdpost" {

  name           =  lookup(var.cicdpost_table_name, terraform.workspace)

  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "cicdpostid"
    type = "S"
  }
  

  hash_key = "cicdpostid"

}


output "cicdpost_table_name" {
  //value = lookup(var.cicdpost_table_name, terraform.workspace)
  value = aws_dynamodb_table.cicdpost.name

}



resource "aws_dynamodb_table" "cicdcomment" {
  
  name           =  lookup(var.cicdcomment_table_name, terraform.workspace)

  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "cicdcommentid"
    type = "S"
  }
  

  hash_key = "cicdcommentid"

}


output "cicdcomment_table_name" {
  value = lookup(var.cicdcomment_table_name, terraform.workspace)
}

```

### lambda.tf

```
resource "aws_iam_role" "CICDS2-TURTIL-APP_lambda_exec" {
  //name = "CICDS2-TURTIL-APP-lambda"
  //name = var.lambda_im_policy

  name = lookup(var.lambda_im_policy, terraform.workspace)



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

resource "aws_iam_role_policy_attachment" "CICDS2-TURTIL-APP_lambda_policy" {
  role       = aws_iam_role.CICDS2-TURTIL-APP_lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
 




resource "aws_iam_policy" "CICDS2-turtil_dynamodb_policy" {
  //name        = var.dynamodb_policy_name
  name        =  lookup(var.dynamodb_policy_name, terraform.workspace)

  description = "Policy allowing basic DynamoDB operations"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
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
resource "aws_iam_role_policy_attachment" "CICDS2-turtil_dynamodb_policy_attachment" {
  policy_arn = aws_iam_policy.CICDS2-turtil_dynamodb_policy.arn
  role       = aws_iam_role.CICDS2-TURTIL-APP_lambda_exec.name

}



resource "random_pet" "lambda_bucket_name" {
  prefix = "lambda"
  length = 2
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket        = random_pet.lambda_bucket_name.id
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "lambda_bucket" {
  bucket                  = aws_s3_bucket.lambda_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


// NOTE: first execute above code by using terraform init , terraform apply then execute below code with same commands

resource "aws_lambda_function" "CICDS2-TURTIL-APP" {
  function_name    = lookup(var.lambda_function_name, terraform.workspace)
  s3_bucket        = aws_s3_bucket.lambda_bucket.id
  s3_key           = aws_s3_object.lambda_CICDS2-TURTIL-APP.key
  runtime          = lookup(var.lambda_runtime, terraform.workspace)
  handler          = lookup(var.lambda_handler, terraform.workspace)
  source_code_hash = data.archive_file.lambda_CICDS2-TURTIL-APP.output_base64sha256
  role             = aws_iam_role.CICDS2-TURTIL-APP_lambda_exec.arn
  timeout          = lookup(var.lambda_timeout, terraform.workspace)
}

resource "aws_cloudwatch_log_group" "CICDS2-TURTIL-APP" {
  name              = "/aws/lambda/${aws_lambda_function.CICDS2-TURTIL-APP.function_name}"
  retention_in_days = lookup(var.lambda_cloudwatch_log_retention, terraform.workspace)
}

data "archive_file" "lambda_CICDS2-TURTIL-APP" {
  type        = "zip"
  source_dir  = "../${path.module}/lambdas/demo_lambda"
  output_path = "../${path.module}/demo_lambda.zip"
}

resource "aws_s3_object" "lambda_CICDS2-TURTIL-APP" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = lookup(var.lambda_s3_key , terraform.workspace)
  source = data.archive_file.lambda_CICDS2-TURTIL-APP.output_path
  etag   = filemd5(data.archive_file.lambda_CICDS2-TURTIL-APP.output_path)
}

// 2nd lambda

resource "random_pet" "lambda_bucket_name2" {
  prefix = "lambda"
  length = 2
}

resource "aws_s3_bucket" "lambda_bucket2" {
  bucket        = random_pet.lambda_bucket_name2.id
  force_destroy = true
}

resource "aws_s3_bucket" "lambda_bucket2" {
  bucket                  = aws_s3_bucket.lambda_bucket2.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

// NOTE: first execute above resource resource "random_pet" "lambda_bucket_name2", resource "aws_s3_bucket" "lambda_bucket2"resource "aws_s3_bucket" "lambda_bucket2" code by using terraform init , terraform apply then execute below code with same commands


resource "aws_lambda_function" "CICDS2-TURTIL-APP2" {
  function_name    = lookup(var.lambda_function_name2, terraform.workspace)
  s3_bucket        = aws_s3_bucket.lambda_bucket2.id
  s3_key           = aws_s3_object.lambda_CICDS2-TURTIL-APP2.key
  runtime          = lookup(var.lambda_runtime2, terraform.workspace)
  handler          = lookup(var.lambda_handler2, terraform.workspace)
  source_code_hash = data.archive_file.lambda_CICDS2-TURTIL-APP2.output_base64sha256
  role             = aws_iam_role.CICDS2-TURTIL-APP_lambda_exec.arn
  timeout          = lookup(var.lambda_timeout2, terraform.workspace)
}

resource "aws_cloudwatch_log_group" "CICDS2-TURTIL-APP2" {
  name              = "/aws/lambda/${aws_lambda_function.CICDS2-TURTIL-APP2.function_name}"
  retention_in_days = lookup(var.lambda_cloudwatch_log_retention2, terraform.workspace)
}





data "archive_file" "lambda_CICDS2-TURTIL-APP2" {
  type        = "zip"
  source_dir  = "../${path.module}/lambdas/demo2_lambda"
  //source_dir  = "/Users/raj/Desktop/my-turtil-repo-18/lambdas/demo2_lambda"

  output_path = "../${path.module}/demo2_lambda.zip"
}






resource "aws_s3_object" "lambda_CICDS2-TURTIL-APP2" {
  bucket = aws_s3_bucket.lambda_bucket2.id
  key    = lookup(var.lambda_s3_key2 , terraform.workspace)
  source = data.archive_file.lambda_CICDS2-TURTIL-APP2.output_path
  etag   = filemd5(data.archive_file.lambda_CICDS2-TURTIL-APP2.output_path)
}



```


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


## api-gateway.tf


```

resource "aws_apigatewayv2_api" "cicd-main" {
  //name          = var.api_name
  name          =  lookup(var.api_name , terraform.workspace)

  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "dev" {
  api_id = aws_apigatewayv2_api.cicd-main.id

  //name        = var.stage_name
  name        =  lookup(var.stage_name , terraform.workspace)

  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.cicd-main_api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_cloudwatch_log_group" "cicd-main_api_gw" {
  name = "/aws/api-gw/${aws_apigatewayv2_api.cicd-main.name}"

  //retention_in_days = var.log_retention_days
  retention_in_days =  lookup(var.log_retention_days, terraform.workspace)

}

resource "aws_apigatewayv2_integration" "lambda_CICDS2-TURTIL-APP" {
  api_id             = aws_apigatewayv2_api.cicd-main.id
  integration_uri    = aws_lambda_function.CICDS2-TURTIL-APP.invoke_arn // change to lambda function name in our case i.e CICDS2-TURTIL-APP
  //integration_uri    = aws_lambda_function.lambda_function_name.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "lambda_CICDS2-TURTIL-APP2" {
  api_id             = aws_apigatewayv2_api.cicd-main.id
  integration_uri    = aws_lambda_function.CICDS2-TURTIL-APP2.invoke_arn // change to lambda function name in our case i.e CICDS2-TURTIL-APP
  //integration_uri    = aws_lambda_function.lambda_function_name.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "add_post_CICDS2-TURTIL-APP" {
  api_id    = aws_apigatewayv2_api.cicd-main.id
  route_key = "POST /add_post"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_CICDS2-TURTIL-APP.id}"
}

resource "aws_apigatewayv2_route" "add_post_CICDS2-TURTIL-APP2" {
  api_id    = aws_apigatewayv2_api.cicd-main.id
  route_key = "POST /add_comment"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_CICDS2-TURTIL-APP2.id}"
}



resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name =  aws_lambda_function.CICDS2-TURTIL-APP.function_name // change to lambda function name in our case i.e CICDS2-TURTIL-APP
  //function_name =  var.lambda_function_name // change to lambda function name in our case i.e CICDS2-TURTIL-APP

  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.cicd-main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "api_gw2" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name =  aws_lambda_function.CICDS2-TURTIL-APP2.function_name // change to lambda function name in our case i.e CICDS2-TURTIL-APP
  //function_name =  var.lambda_function_name // change to lambda function name in our case i.e CICDS2-TURTIL-APP

  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.cicd-main.execution_arn}/*/*"
}

output "TURTIL-APP_base_url" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}

```

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


## custom-domain.tf


```

# Create TLS certificate
resource "aws_acm_certificate" "api" {
  //domain_name       = var.domain_name
  //validation_method = var.validation_method

  domain_name       =  lookup(var.domain_name , terraform.workspace)
  validation_method =  lookup(var.validation_method , terraform.workspace)

}

# Retrieve Route53 zone
data "aws_route53_zone" "public" {
  //name         = var.route53_zone_name

  name         =  lookup(var.route53_zone_name , terraform.workspace)

  private_zone = false
}

# Create Route53 record for certificate validation
resource "aws_route53_record" "api_validation" {
  for_each        = { for dvo in aws_acm_certificate.api.domain_validation_options : dvo.domain_name => dvo }
  allow_overwrite = true
  name            = each.value.resource_record_name
  records         = [each.value.resource_record_value]
  //ttl             = var.route53_ttl

  ttl             =  lookup(var.route53_ttl , terraform.workspace)

  type            = each.value.resource_record_type
  zone_id         = data.aws_route53_zone.public.zone_id
}

# Validate ACM certificate
resource "aws_acm_certificate_validation" "api" {
  certificate_arn         = aws_acm_certificate.api.arn
  validation_record_fqdns = [for record in aws_route53_record.api_validation : record.fqdn]
}

# Create API Gateway domain name
resource "aws_apigatewayv2_domain_name" "api" {
  //domain_name = var.domain_name

  domain_name =  lookup(var.domain_name, terraform.workspace)


  domain_name_configuration {
    certificate_arn = aws_acm_certificate.api.arn
    //endpoint_type   = var.endpoint_type
    //security_policy = var.security_policy

    endpoint_type   =  lookup(var.endpoint_type, terraform.workspace)
    security_policy =  lookup(var.security_policy, terraform.workspace)
  }

  depends_on = [aws_acm_certificate_validation.api]
}

# Create Route53 record for API Gateway domain
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

# Create API Gateway mappings
resource "aws_apigatewayv2_api_mapping" "api" {
  api_id      = aws_apigatewayv2_api.cicd-main.id
  domain_name = aws_apigatewayv2_domain_name.api.id
  stage       = aws_apigatewayv2_stage.dev.id
  //stage       = var.environment == "development" ? aws_apigatewayv2_stage.dev.id: aws_apigatewayv2_stage.PROD.id

  
}

resource "aws_apigatewayv2_api_mapping" "api_v1" {
  api_id          = aws_apigatewayv2_api.cicd-main.id
  domain_name     = aws_apigatewayv2_domain_name.api.id
  stage           = aws_apigatewayv2_stage.dev.id
  //stage       = var.environment == "development" ? aws_apigatewayv2_stage.dev.id: aws_apigatewayv2_stage.PROD.id

  //api_mapping_key = var.api_mapping_key
  api_mapping_key =  lookup(var.api_mapping_key, terraform.workspace)

}

# Outputs
output "custom_domain_api" {
  value = "https://${aws_apigatewayv2_api_mapping.api.domain_name}"
}

output "custom_domain_api_v1" {
  value = "https://${aws_apigatewayv2_api_mapping.api_v1.domain_name}/${aws_apigatewayv2_api_mapping.api_v1.api_mapping_key}"
}



```

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

## Create a Dev Envinorment
Execute the following command to apply the configuration:

```
terraform workspace new dev

```

## Create a Prod Envinorment
Execute the following command to apply the configuration:

```
terraform workspace new prod

```

## check Dev and Prod Envinorment create
Execute the following command to apply the configuration:

```
terraform workspace list

```

## push the code to codecommit repo 
Execute the following command to apply the configuration:

```
cd ..

```

```
git checkout -b main

```

```
git branch 

```

```
git add .

```


```
git commit -m "my first commit"

```


```
git push origin main

```

```
git tag v1.0

```

```
git push origin v1.0

```


## go to code pipeline the output should be like this

<img width="1440" alt="Screenshot 2024-03-07 at 10 54 51 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/afed0dd2-550c-4064-bf09-8ac8dbd95ac2">



<img width="1440" alt="Screenshot 2024-03-07 at 10 55 00 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/19a6a9c6-8bf1-4793-867d-247fd94b2969">


<img width="1440" alt="Screenshot 2024-03-07 at 10 55 04 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/6b197f3f-6c19-471c-83b3-ac90f63f564e">



# how to create a git tag roll-back by codebuild in codecommit repo

# step-1 create a roll back branch in codecommit

<img width="1440" alt="Screenshot 2024-03-07 at 11 16 09 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/39169f24-6863-40d4-b3be-91d02626ff20">


<img width="1440" alt="Screenshot 2024-03-07 at 11 16 21 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/3fab9f43-4aca-47ae-a3e4-5e9454049485">



<img width="1440" alt="Screenshot 2024-03-07 at 11 22 44 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/811c01ab-ef31-4a69-a944-227b64fe87e6">


<img width="1440" alt="Screenshot 2024-03-07 at 11 23 09 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/80808aad-7bc5-4336-acb0-7e176e5338bd">

<img width="1440" alt="Screenshot 2024-03-07 at 11 23 41 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/61e8dd3f-812a-44d8-a2c2-e214db0eb617">


# step-2 create a build project for roll back branch in codebuild

<img width="1440" alt="Screenshot 2024-03-07 at 11 31 07 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/e6716602-75a2-4954-aa1a-e4aaa4d0d71f">

<img width="1440" alt="Screenshot 2024-03-07 at 11 32 15 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/f5311ba7-7ce5-43a7-a4de-2608a72a3d6b">

<img width="1440" alt="Screenshot 2024-03-07 at 11 39 19 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/bb835b65-db3f-4ee8-b365-fee2e52ffab8">


### scroll down

<img width="1440" alt="Screenshot 2024-03-07 at 11 34 03 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/156cec53-6fcf-441f-b70b-88beba59537a">


### scroll down

<img width="1440" alt="Screenshot 2024-03-07 at 11 34 27 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/0e5b4184-429e-4aff-a1fb-9a088c53cfee">


<img width="980" alt="Screenshot 2024-03-07 at 11 34 55 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/ef22348e-4a27-47b1-b0f9-13aec1ecdc81">

###  give your own aws credentials or copy above picture details in below

<img width="1440" alt="Screenshot 2024-03-07 at 11 35 05 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/2ad2f4bd-ec8f-41df-ab7a-e8cff1274c47">

```

version: 0.2

phases:
  build:
    commands:
      
      - aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
      - aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
      - aws configure set region $AWS_REGION
      
      - git config --global credential.helper '!aws codecommit credential-helper $@'
      - git config --global credential.UseHttpPath true
      
      - git config --global user.email "rajsekhar.s@turtil.co"
      - git config --global user.name "rajsekhar"
      
      - ls
     
      - git branch
      - git checkout main
      - ls
      
      - git tag
      
      - TAG=$(git for-each-ref refs/tags --sort=-creatordate --format '%(refname:short)' | sed -n '2p')
      
      - git branch
      
      - git checkout $TAG
      - ls
      - git branch
      
      - git push -f origin $TAG:main



```

### copy and paste the above code as shown in below image

<img width="1440" alt="Screenshot 2024-03-07 at 11 35 14 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/43be6bc4-4f78-4ed8-9814-3e7c9683fb65">

### scroll down

<img width="1440" alt="Screenshot 2024-03-07 at 11 35 28 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/c61668d2-fb49-461f-bbff-75f356be632a">


<img width="1440" alt="Screenshot 2024-03-07 at 11 35 31 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/693de1b9-13de-451f-9b77-387cbd55fb0d">


<img width="1440" alt="Screenshot 2024-03-07 at 11 35 53 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/b90565f8-5bd1-4a97-974d-df0a9848c1b5">

# Note: Rollback only work when push the code with git tags

### check code rollbacked in main branch with previous git tag
<img width="1440" alt="Screenshot 2024-03-07 at 11 51 51 AM" src="https://github.com/tortoise-NRI/Backend-poc/assets/153161379/f54728cc-afa7-4413-a39f-2cd50d77b36c">
