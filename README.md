# How to Create Ec2 instance

### click on launch instances

<img width="1440" alt="Screenshot 2023-12-26 at 7 22 52 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/a8795da8-9b43-43c5-bbd6-f0947d94e9ad">

### enter a your own name in our case jenkin

<img width="1440" alt="Screenshot 2023-12-26 at 7 57 47 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/d5bcd87e-76db-4f76-aab4-0fe94b005b82">

### select ubuntu OS in Application and OS Images

<img width="1440" alt="Screenshot 2023-12-26 at 7 57 56 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/db80db92-89d7-45d6-ba58-d8c84e7dc5b7">

### select instance type in our case we are selecting t2-medium

<img width="1440" alt="Screenshot 2023-12-26 at 7 58 13 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/a9c4ebda-c6c4-448e-bef6-92044b285459">

### click on create new key pair 

<img width="1440" alt="Screenshot 2023-12-26 at 7 58 26 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/9b9191cc-d5d5-4150-842d-a8b4b77e4e19">

### enter your own key pair name in our case we have jenkin-demo and click on create key pair 

<img width="1440" alt="Screenshot 2023-12-26 at 7 58 49 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/66e01a4b-e1e5-45ba-8c6b-b46d840f2db9">

###  In Network Settings click on Allow HTTPS traffic from the internet and click on Allow HTTP traffic from the internet

<img width="1440" alt="Screenshot 2023-12-26 at 7 59 04 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/7168da24-d2e7-4118-a070-8dd7029a91af">

### in configure stroage enter 30gb and select general purpose SSD(gp3) and CLICK ON Launch instance

<img width="1440" alt="Screenshot 2023-12-26 at 7 59 24 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/3718e824-4565-46ec-82e6-6a9b0d5a1893">




# 1. Installing Jenkins

First, update the default Ubuntu packages lists for upgrades with the following command:
```bash
sudo apt-get update
```
Then, run the following command to install JDK 11:
```bash
sudo apt install fontconfig openjdk-17-jre
```
Now, we will install Jenkins itself. Issue the following four commands in sequence to initiate the installation from the Jenkins repository:
```bash
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian/jenkins.io-2023.key
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt-get update

sudo apt-get install jenkins

```
Once that’s done, start the Jenkins service with the following command:
```bash
sudo systemctl start jenkins.service
```
To confirm its status, use:
```bash
sudo systemctl status jenkins
```
With Jenkins installed, we can proceed with adjusting the firewall settings. By default, Jenkins will run on port 8080.

In order to ensure that this port is accessible, we will need to configure the built-in Ubuntu firewall (ufw). To open the 8080 port and enable the firewall, use the following commands:
```bash
sudo ufw allow 8080
```
```bash
sudo ufw enable
```
Once done, test whether the firewall is active using this command:
```bash
sudo ufw status
```
# Enable port 8080 in inbound rules of security groups

### click the ec2 instance in our case jenkin

<img width="1440" alt="Screenshot 2023-12-26 at 7 22 58 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/317d4122-5ca1-4ff2-a78f-b75dab77c77f">

### scroll down

<img width="1440" alt="Screenshot 2023-12-26 at 7 23 12 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/c180ff0d-5692-4db6-9963-0e61084bce1e">

### click on security

<img width="1440" alt="Screenshot 2023-12-26 at 7 23 25 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/c4c7e910-eb16-4286-a0fe-380f80d39997">

### click on security groups

<img width="1440" alt="Screenshot 2023-12-26 at 7 23 34 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/b25f8fcb-b646-45bf-b695-c2ac0ea848b2">

### click on edit inbound rules

 - click on Add rule
 - select Type Custom TCP
 - Enter port range 8080
 - select source Custom and select 0.0.0.0/0
 - click save rules




<img width="1440" alt="Screenshot 2023-12-26 at 7 24 32 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/5b1e2e7b-7c05-432a-90b5-2426f5d1ed9a">







With the firewall configured, it’s time to set up Jenkins itself. Type in the IP of your EC2 along with the port number. The Jenkins setup wizard will open.

Ec2 ip = 13.233.232.6

port = 8080

http://13.233.232.67:8080/

<img width="1440" alt="Screenshot 2023-12-26 at 7 51 33 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/ce02a4db-e481-4863-80a6-c616c9e76350">


To check the initial password, use the cat command as indicated below:
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

All Set! You can now start automating...

# 2. How to Give Jenkins sudo Permissions


### Step 1: Access sudoers file
Open the terminal on the system where Jenkins is installed.
Run the command: sudo visudo. This command edits the sudoers file safely.
```bash
sudo visudo

```

### Step 2: Edit sudoers file
Find the line that contains the list of user privileges. It typically looks like:

```bash
root    ALL=(ALL:ALL) ALL

```
Below the root entry, add a line granting sudo access to Jenkins. Replace <jenkins_username> with the actual username of your Jenkins user:

```bash
<jenkins_username>  ALL=(ALL:ALL) NOPASSWD: ALL # in our case 'jenkins'. replace  <jenkins_username>  with name jenkins

```
### Ex: jenkins  ALL=(ALL:ALL) NOPASSWD: ALL


### Step 3: Save and exit
Press Ctrl + X to exit the editor.
Confirm to save changes by typing Y and press Enter.
Verify the sudoers file by running sudo visudo -c to check for syntax errors.

```bash
sudo visudo -c 
```

### Step 4: Restart Jenkins service
Restart the Jenkins service to apply the changes made to the sudoers file.

```bash
sudo service jenkins restart

```

# 3. How To Create a Route53

## We need to get a domain/subdomain from Route53.

1. Click on hosted zones

   <img width="1440" alt="Screenshot 2023-12-26 at 6 11 36 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/e2ba197d-51c3-4f5e-bafc-fe67b25a62e5">

2. Click on hosted zones. In this case "turtil.co"

   <img width="1440" alt="Screenshot 2023-12-26 at 6 11 48 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/8a6b827c-fb47-4e58-bf5b-d160fa899349">

3. Click on create record. 
Enter the record name. Here we are creating a subdomain: devjenkins
Select as A-Route because we are adding IP address as the value in Alias section
Enter the value. Here we are giving ec2 public ip address: 13.233.232.67
select 1d in TTL(seconds) sections.
click on Create records.

<img width="1440" alt="Screenshot 2023-12-26 at 6 13 22 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/ce9288f1-ac1a-4453-a063-0c9737a97904">


      

# 4. How to add Secured Custom domains for jenkins


### Nginx Webserver is installation
Install Nginx: Install Nginx using the following command:

```bash

sudo apt install nginx

```
Start Nginx: Once the installation is complete, start the Nginx service:

```bash
sudo service nginx start
```
To check the nginx status 

```bash
sudo service nginx status

```
This command starts the Nginx service, and it will now be running on your EC2 instance.
Enable Nginx to Start on Boot: To ensure Nginx starts automatically when your server restarts, enable it as a startup service:

```bash
sudo systemctl enable nginx
```
Verify Nginx Installation: Open your web browser and enter your EC2 instance's public IP address or domain name. You should see the default Nginx welcome page, indicating that Nginx is successfully installed and running.


<img width="1440" alt="Screenshot 2023-12-26 at 7 43 58 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/22dc7d03-c5ba-4d7c-af1c-db9c90927729">






### Create a Jenkins Server Block:
Create a new Nginx server block configuration file for Jenkins. You can do this by creating a new file in the /etc/nginx/sites-available/ directory. Let's name it jenkins:

```bash
sudo nano /etc/nginx/sites-available/jenkins
```

Config File
```bash
server {
    listen 80;
    server_name jenkins.example.com; # Replace with your domain

    location / {
        proxy_pass http://localhost:8080; # Jenkins is running on the default port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~ /\. {
        deny all;
    }
}

```

###  Enable the Jenkins Server Block:
Create a symbolic link to the configuration file in the sites-enabled directory:
```bash
sudo ln -s /etc/nginx/sites-available/jenkins /etc/nginx/sites-enabled/
```

Test Nginx Configuration:
	•	Before restarting Nginx, it's a good idea to test the configuration to make sure there are no syntax errors:
 ```bash
sudo nginx -t
```
If the test is successful, you should see: nginx: configuration file /etc/nginx/nginx.conf test is successful.
	•	Restart Nginx: Restart Nginx to apply the changes:
 ```bash
sudo systemctl restart nginx
```
	•	Access Jenkins: Open your web browser and navigate to http://jenkins.example.com. Replace jenkins.example.com with your actual domain. You should now be able to access Jenkins through Nginx.


### SSL certificate applied to Domain .

 ```bash
sudo apt install python3-certbot-nginx
 ```

 ```bash
certbot --version
 ```

 ```bash
sudo su
 ```

 ```bash
certbot --nginx -d xyz.com # xyz.com in place give your own domain our case we given 'devjenkins.turtil.co'

 ```


That’s all. Now on, your Jenkins server will run by Secured Custom domain.


# How to install terraform plugin


### click on  manage jenkins

<img width="1440" alt="Screenshot 2023-12-26 at 9 47 46 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/53966bc9-8627-471b-837f-69030b2f8298">

### select plugins

<img width="1440" alt="Screenshot 2023-12-27 at 8 52 48 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/52b379e2-987a-4de1-a65c-a29260bf09d0">

### click on Available plugins enter terraform and select terraform-plugin and install it

<img width="1440" alt="Screenshot 2023-12-27 at 8 53 12 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/4d08cf45-cd84-420c-b721-fc5c0b4e5755">


# How to install terraform in aws ubuntu and Configure to jenkins


### click this link  https://developer.hashicorp.com/terraform/install and copy link 

<img width="1440" alt="Screenshot 2023-12-26 at 9 56 43 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/ae57bbd8-b8c7-4b29-bcf6-43a0fb1bd0e8">

### sudo wget https://releases.hashicorp.com/terraform/1.6.6/terraform_1.6.6_linux_amd64.zip

```bash
sudo wget https://releases.hashicorp.com/terraform/1.6.6/terraform_1.6.6_linux_amd64.zip

```

<img width="1440" alt="Screenshot 2023-12-26 at 9 57 51 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/fe9f71bb-97e0-492c-9893-5a85d4fc7913">

### check whether package is downloaded

```bash
sudo ls

```
<img width="563" alt="Screenshot 2023-12-26 at 9 58 54 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/5212ed3c-bab3-4161-b9be-e6df683569fa">

### install unzip

```bash
sudo apt-get install unzip

```

### unzip downloaded package

```bash
sudo unzip terraform_1.6.5_darwin_arm64.zip 

```

### check whether package is uzipped

```bash
sudo ls

```
### set the enviromental variables copy the uzip folder to /usr/bin

```bash
sudo mv terraform /usr/bin

```
### check whether terrafrom is installed or not 

```bash
terraform

```

### get the path  and paste path only this /usr/bin/ in jenkins tools 

```bash
which terraform

```

### Go to jenkins

### click on  manage jenkins

<img width="1440" alt="Screenshot 2023-12-26 at 9 47 46 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/53966bc9-8627-471b-837f-69030b2f8298">


### select Tools

<img width="1440" alt="Screenshot 2023-12-27 at 8 54 12 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/23b08aed-433c-4c9f-a492-6ff0cca5edc3">

### scroll down

<img width="1440" alt="Screenshot 2023-12-27 at 8 54 18 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/1f5fb819-3fd5-4f9c-ac4a-4283856413a4">

### select Terraform Installations

<img width="1440" alt="Screenshot 2023-12-27 at 8 54 33 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/5bdfe0d6-7607-4a7d-97a0-20386a6902e4">

### Enter the Name in our case terraform and Enter path /usr/bin/ in Install Directory  and click save 

<img width="1440" alt="Screenshot 2023-12-27 at 8 54 44 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/1edb1755-44f5-4a54-8940-889698c7b6d9">





# How to create jobs in jenkins

### click on New item

<img width="1440" alt="Screenshot 2023-12-26 at 9 42 04 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/441554c7-e4c8-469c-aa9b-6dfc95645d5c">

### Enter a item name in our case terraform-demo and select pipline and click ok

<img width="1440" alt="Screenshot 2023-12-26 at 9 42 42 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/c8c4c5b4-53dc-4fe3-870b-25ea5796e778">

### give any description 

<img width="1440" alt="Screenshot 2023-12-26 at 9 42 53 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/635ee11f-cd71-41e0-a836-358226ebad86">

### scroll down and select pipeline script

<img width="1440" alt="Screenshot 2023-12-26 at 9 43 14 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/621ce61b-3833-409e-800f-dad0430f51ce">



```bash

pipeline {

    environment {
        AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

    }

   agent  any
     stages {
        stage ("checkout from GIT") {
            steps {
                git branch: 'main', credentialsId: 'rajsekhar', url: 'https://github.com/tortoise-NRI/Backend-poc.git'
            }
        }

        stage("Install Python dependencies and create zip") {
            steps {
                    script {

                        sh  '''
                            sudo apt-get update
                            sudo apt-get install -y python3 python3-pip zip
                            sudo rm -rf python
                            sudo mkdir python
                            sudo pip3 install -r requirements.txt -t python/
                            sudo zip -r python.zip python/
                        '''

                    }
                }
            }

       
        stage ("terraform init") {
            steps {
                sh 'terraform init'
            }
        }
        stage ("terraform fmt") {
            steps {
                sh 'terraform fmt'
            }
        }
        stage ("terraform validate") {
            steps {
                sh 'terraform validate'
            }
        }
        stage ("terrafrom plan") {
            steps {
                sh 'terraform plan '
            }
        }
        stage ("terraform apply") {
            steps {
                sh 'terraform apply --auto-approve'
            }
        }
    }

  }

```

### copy the above script anmd paste here like this and click save

<img width="1440" alt="Screenshot 2023-12-26 at 9 45 43 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/464bd509-7611-4bb9-95c5-3fb6f6385b0f">



# How to create a  AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for PIPELINE SCRIPT

### click on  manage jenkins

<img width="1440" alt="Screenshot 2023-12-26 at 9 47 46 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/53966bc9-8627-471b-837f-69030b2f8298">

### click on credentials

<img width="1440" alt="Screenshot 2023-12-26 at 10 18 24 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/00ba9354-3f10-4d37-83c1-e644cc2813c8">


### click on global credentials

<img width="1440" alt="Screenshot 2023-12-26 at 10 18 45 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/f413ec88-591e-40de-8a62-02875f1bfbce">

### click on Add credentails

<img width="1440" alt="Screenshot 2023-12-26 at 10 19 23 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/52d314ce-32a9-4a1b-808f-da4a530b84dd">

### select kind secret text

<img width="1440" alt="Screenshot 2023-12-26 at 10 19 45 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/4abdc461-2a0d-4ede-bd48-1686a68b9d24">

### for AWS_ACCESS_KEY_ID: enter ID in our case AWS_ACCESS_KEY_ID, enter DESCRIPTION in our case AWS_ACCESS_KEY_ID,enter your  own aws_access_key_id in secret and click create

<img width="1440" alt="Screenshot 2023-12-26 at 10 20 50 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/50877070-ba21-4f63-837f-e6ab2866804c">

### for AWS_SECRET_ACCESS_KEY: enter ID in our case AWS_SECRET_ACCESS_KEY, enter DESCRIPTION in our case AWS_SECRET_ACCESS_KEY,enter your  own aws_secret_access_key in secret and click create

<img width="1440" alt="Screenshot 2023-12-26 at 10 21 39 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/17d0c835-08fc-4fae-b7e8-4a9f061ce6f3">


# How to create credentialsId for PIPELINE SCRIPT


### go to github repo select settings

<img width="1440" alt="Screenshot 2023-12-27 at 7 49 37 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/011e6f9f-c347-4ee0-831c-cab1567ba6c2">

### scroll down

<img width="1440" alt="Screenshot 2023-12-27 at 7 50 00 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/cf0c518e-b10b-4b52-b7e7-10fbd66905c3">


### select developer settings

<img width="1440" alt="Screenshot 2023-12-27 at 7 50 20 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/e209a7e9-69f1-4918-b563-a460fe4c4d27">


### click on personal access token

<img width="1440" alt="Screenshot 2023-12-27 at 7 50 30 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/23275981-2f01-4759-820b-2c0d0a7a1dba">

### click on Tokens(classic)

<img width="1440" alt="Screenshot 2023-12-27 at 7 50 43 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/08814863-61dc-46c5-988d-623c09ef94c2">

### click on Generate new token

<img width="1440" alt="Screenshot 2023-12-27 at 7 51 11 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/26a885cc-354e-4c6f-88b0-cb46fdf940ac">

### click on generate new token(classic)

<img width="1440" alt="Screenshot 2023-12-27 at 7 51 23 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/b79a6e53-72b3-437f-aa09-f2f571d79d5f">

### enter your password and click confirm

<img width="1440" alt="Screenshot 2023-12-27 at 7 51 56 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/c2d216a6-8ef2-459a-9b08-2ffb0c4ae3f9">


### Enter a name in  the NOTE and our case git-demo-token and select EXPIRATION  no expire

<img width="1440" alt="Screenshot 2023-12-27 at 7 52 46 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/754ff19c-7d49-4f73-bdaa-5d39fdc5564d">

### select All Scopes 

<img width="1440" alt="Screenshot 2023-12-27 at 7 53 45 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/43ed4bb4-bf90-471f-a008-e720e8787c89">


### Scroll down click Generate token

<img width="1440" alt="Screenshot 2023-12-27 at 7 53 55 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/44c45077-a514-4b6b-aa6b-9a0da4d7e27f">


### Copy the token : the token should look like this " ghp_7############lm "

### Go to jenkins home page 

### click on  manage jenkins

<img width="1440" alt="Screenshot 2023-12-26 at 9 47 46 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/53966bc9-8627-471b-837f-69030b2f8298">

### click on credentials

<img width="1440" alt="Screenshot 2023-12-26 at 10 18 24 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/00ba9354-3f10-4d37-83c1-e644cc2813c8">


### click on global credentials

<img width="1440" alt="Screenshot 2023-12-26 at 10 18 45 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/f413ec88-591e-40de-8a62-02875f1bfbce">

### click on Add credentails

<img width="1440" alt="Screenshot 2023-12-26 at 10 19 23 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/52d314ce-32a9-4a1b-808f-da4a530b84dd">

### select kind username with password

<img width="1440" alt="Screenshot 2023-12-27 at 8 24 51 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/66444fa2-7238-48c8-be27-8ba64809f505">

### Enter your  user name in our case rajsekhar222(github username) 
### Enter your ID in our case rajsekhar,
### Enter your password in our case paste token from git in password (the password will be this " ghp_7############lm " which we copied from git )
### click create 

<img width="1440" alt="Screenshot 2023-12-27 at 8 26 47 AM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/1fa04c82-5bb3-4a5d-adbd-d40b37529caf">

 ### git branch: 'main', 
 
 ### credentialsId: 'rajsekhar', 
 
 ### url: 'https://github.com/tortoise-NRI/



### click on build 

<img width="1440" alt="Screenshot 2023-12-26 at 9 47 24 PM" src="https://github.com/yeshwanthlm/installing-jenkins/assets/153161379/c0f336f2-e385-4bbf-9cc2-499aa5284737">











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


# Create Lambda Layer
resource "aws_lambda_layer_version" "my_lambda_layer" {
  filename             = "python.zip"  # Replace with the path to your ZIP file
  layer_name           = "my_lambda_layer"
  compatible_runtimes  = ["python3.11"]  # Replace with your desired Python version
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

  # Attach Lambda Layer
  layers = [aws_lambda_layer_version.my_lambda_layer.arn]
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



//resource "aws_iam_policy_attachment" "dynamodb_policy_attachment" {
  //name       = "DynamoDBPolicyAttachment"
  //roles       = aws_iam_role.BACKEND-POC_lambda_exec.name
  //roles      = [aws_iam_role.dynamodb_policy.id] // Replace with your DynamoDB role name
  //policy_arn = aws_iam_policy.dynamodb_policy.arn
  //policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
//}


// to create cognito user
resource "aws_iam_policy" "cognito_admin_create_user_policy" {
  name        = "CognitoAdminCreateUserPolicy"
  description = "Policy allowing AdminCreateUser in Cognito User Pool"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Action    = "cognito-idp:AdminCreateUser",
      Resource  = "arn:aws:cognito-idp:us-east-1:033464272864:userpool/us-east-1_EUHla6BwY"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "cognito_admin_create_user_attachment" {
  policy_arn = aws_iam_policy.cognito_admin_create_user_policy.arn
  role       = aws_iam_role.BACKEND-POC_lambda_exec.name
}

// to create password
resource "aws_iam_policy" "cognito_admin_set_password_policy" {
  name        = "CognitoAdminSetPasswordPolicy"
  description = "Policy allowing AdminSetUserPassword in Cognito User Pool"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Action    = "cognito-idp:AdminSetUserPassword",
        Resource  = "arn:aws:cognito-idp:us-east-1:033464272864:userpool/us-east-1_EUHla6BwY"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "cognito_admin_set_password_attachment" {
  policy_arn = aws_iam_policy.cognito_admin_set_password_policy.arn
  role       = aws_iam_role.BACKEND-POC_lambda_exec.name
}

```



The infrastructure provisioned includes:

- **Random Pet Name Generation**: Creates a random prefix-based name for the S3 bucket.
- **S3 Bucket for Lambda**: Defines an S3 bucket to store the Lambda function's code.
- **Public Access Block for S3 Bucket**: Restricts public access to the S3 bucket.
- **Lambda Layer: Defines a Lambda layer for the specified Python runtime.
- **IAM Role for Lambda Execution**: Grants necessary permissions to the Lambda function for execution.
- **IAM Role Policy Attachment**: Attaches an AWS managed policy to the Lambda execution role.
- **Lambda Function**: Deploys the Lambda function using the specified runtime and handler.
- **CloudWatch Log Group**: Sets up a log group for Lambda function logs.
- **Archive File and S3 Object**: Archives the Lambda function code and uploads it to the S3 bucket.
- **IAM Policy for DynamoDB**: Defines a custom policy allowing basic DynamoDB operations.
- **IAM Policy Attachment to Lambda's Role**: Attaches the DynamoDB policy to the Lambda execution role.
- **IAM Policy for Cognito AdminCreateUser (`aws_iam_policy.cognito_admin_create_user_policy`):** Defines a policy allowing AdminCreateUser in a Cognito User Pool.
- **IAM Role Policy Attachment for Cognito AdminCreateUser (`aws_iam_role_policy_attachment.cognito_admin_create_user_attachment`):** Attaches the Cognito AdminCreateUser policy to the Lambda's execution role.
- **IAM Policy for Cognito AdminSetUserPassword (`aws_iam_policy.cognito_admin_set_password_policy`):** Defines a policy allowing AdminSetUserPassword in a Cognito User Pool.
- **IAM Role Policy Attachment for Cognito AdminSetUserPassword (`aws_iam_role_policy_attachment.cognito_admin_set_password_attachment`):** Attaches the Cognito AdminSetUserPassword policy to the Lambda's execution role.

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
### `Lambda Layer` Resource

create a Lambda layer for the specified Python runtime.

```
# Create Lambda Layer
resource "aws_lambda_layer_version" "my_lambda_layer" {
  filename             = "python.zip"  # Replace with the path to your ZIP file
  layer_name           = "my_lambda_layer"
  compatible_runtimes  = ["python3.11"]  # Replace with your desired Python version
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

### IAM Policy for Cognito AdminCreateUser (`aws_iam_policy.cognito_admin_create_user_policy`)
Defines a policy allowing AdminCreateUser in a Cognito User Pool.

```
// to create cognito user
resource "aws_iam_policy" "cognito_admin_create_user_policy" {
  name        = "CognitoAdminCreateUserPolicy"
  description = "Policy allowing AdminCreateUser in Cognito User Pool"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Action    = "cognito-idp:AdminCreateUser",
      Resource  = "arn:aws:cognito-idp:us-east-1:033464272864:userpool/us-east-1_EUHla6BwY"
    }]
  })
}

```

### IAM Role Policy Attachment for Cognito AdminCreateUser (`aws_iam_role_policy_attachment.cognito_admin_create_user_attachment`)
Attaches the Cognito AdminCreateUser policy to the Lambda's execution role.

```

resource "aws_iam_role_policy_attachment" "cognito_admin_create_user_attachment" {
  policy_arn = aws_iam_policy.cognito_admin_create_user_policy.arn
  role       = aws_iam_role.BACKEND-POC_lambda_exec.name
}

```


### IAM Policy for Cognito AdminSetUserPassword (`aws_iam_policy.cognito_admin_set_password_policy`)
Defines a policy allowing AdminSetUserPassword in a Cognito User Pool.

```
// to create password
resource "aws_iam_policy" "cognito_admin_set_password_policy" {
  name        = "CognitoAdminSetPasswordPolicy"
  description = "Policy allowing AdminSetUserPassword in Cognito User Pool"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Action    = "cognito-idp:AdminSetUserPassword",
        Resource  = "arn:aws:cognito-idp:us-east-1:033464272864:userpool/us-east-1_EUHla6BwY"
      }
    ]
  })
}

```


### IAM Role Policy Attachment for Cognito AdminSetUserPassword (`aws_iam_role_policy_attachment.cognito_admin_set_password_attachment`)
Attaches the Cognito AdminSetUserPassword policy to the Lambda's execution role.

```

resource "aws_iam_role_policy_attachment" "cognito_admin_set_password_attachment" {
  policy_arn = aws_iam_policy.cognito_admin_set_password_policy.arn
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


# step 4

# AWS Lambda Layer with Terraform

This Terraform script creates an AWS Lambda Layer to share common libraries, dependencies, or code across multiple Lambda functions. 

## Overview

AWS Lambda Layers are a way to centralize and manage common code, libraries, and dependencies that multiple Lambda functions may use. This Terraform script demonstrates the creation of an AWS Lambda Layer that can be attached to Lambda functions.

## Prerequisites

Before using this Terraform script, ensure you have the following:
- An AWS account with appropriate permissions to create Lambda Layers using Terraform.
- Terraform installed locally. You can download it from [Terraform's official website](https://www.terraform.io/downloads.html).
- A ZIP file containing the necessary Python libraries or code that you want to include in the Lambda Layer. Ensure it is named `python.zip` or update the `filename` field in the script accordingly.

## Configuration

```

# Create Lambda Layer
resource "aws_lambda_layer_version" "my_lambda_layer" {
  filename             = "python.zip"  # Replace with the path to your ZIP file
  layer_name           = "my_lambda_layer"
  compatible_runtimes  = ["python3.11"]  # Replace with your desired Python version
}


//output "layer_arn" {
  //value = aws_lambda_layer_version.my_lambda_layer.arn
//}

```

1. **File Structure:**

    Place the `python.zip` file containing the Python libraries or code in the same directory where you have the Terraform script (`.tf` file). If the ZIP file is located elsewhere, update the `filename` field in the Terraform script with the correct path.

2. **Edit Terraform Script:**

    - Open the `main.tf` or your Terraform script file.
    - Locate the resource block for `aws_lambda_layer_version`.
    - Update the `filename` attribute with the correct path to your `python.zip` file.
    - Optionally, modify the `layer_name` and `compatible_runtimes` according to your requirements.

## Usage

1. **Initialize Terraform:**

    ```bash
    terraform init
    ```

2. **Review Changes:**

    Check the changes Terraform will make before applying them:

    ```bash
    terraform plan
    ```

3. **Apply Changes:**

    If everything looks correct, apply the changes to create the Lambda Layer:

    ```bash
    terraform apply
    ```

4. **Cleanup (Optional):**

    To remove the created Lambda Layer:

    ```bash
    terraform destroy
    ```

## Resources

- [Terraform Documentation](https://www.terraform.io/docs/index.html)
- [AWS Lambda Layers Documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)

## License

This Terraform script is licensed under [MIT License](LICENSE).




# step 5

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


# step 6

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



# step 7

# AWS API Gateway with Lambda Integration and Cognito Authorization

This Terraform code creates an AWS API Gateway, integrating it with AWS Lambda functions and setting up Cognito-based authorization for secure API access.

## Prerequisites

- **AWS Account:** Ensure you have an AWS account and necessary permissions.
- **Terraform:** Install Terraform to manage the infrastructure.
- **AWS CLI:** Configure AWS CLI with appropriate credentials.

## Structure

The code consists of the following main resources:

- **AWS API Gateway (`aws_apigatewayv2_api`):**
  - Creates an HTTP API named "main."

- **API Stages (`aws_apigatewayv2_stage`):**
  - Defines a "dev" stage for the API and enables auto-deployment.
  - Configures access logs to stream into CloudWatch for monitoring.

- **CloudWatch Log Group (`aws_cloudwatch_log_group`):**
  - Creates a log group to store API Gateway access logs.

- **Lambda Integration (`aws_apigatewayv2_integration`):**
  - Integrates Lambda function ("BACKEND-POC") with the API using AWS_PROXY for POST requests.

- **Cognito Authorizer (`aws_apigatewayv2_authorizer`):**
  - Sets up a JWT-based authorizer using Cognito for API authorization.

- **API Routes (`aws_apigatewayv2_route`):**
  - Defines various routes for different HTTP methods (GET, POST, DELETE) with associated integration and authorization.

- **Lambda Permission (`aws_lambda_permission`):**
  - Grants API Gateway permission to invoke the Lambda function.

## Configuration

```

resource "aws_apigatewayv2_api" "main" {
  name          = "main"  // give your own name
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "dev" {
  api_id = aws_apigatewayv2_api.main.id

  name        = "dev" // give your own name
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.main_api_gw.arn

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

resource "aws_cloudwatch_log_group" "main_api_gw" {
  name = "/aws/api-gw/${aws_apigatewayv2_api.main.name}"

  retention_in_days = 14
}

variable "AWS_REGION" {
  description = "The AWS region where resources will be deployed"
  default     = "us-east-1"  # Set your preferred default AWS region here
}



resource "aws_apigatewayv2_integration" "lambda_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.BACKEND-POC.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_authorizer" "cognito_authorizer" {
  api_id             = aws_apigatewayv2_api.main.id
  name               = "cognito-authorizer"
  authorizer_type    = "JWT"
  identity_sources   = ["$request.header.Authorization"]  # Assuming JWT token is in the Authorization header
  jwt_configuration {
    issuer             = "https://cognito-idp.${var.AWS_REGION}.amazonaws.com/${aws_cognito_user_pool.user_pool.id}"
    audience           = [aws_cognito_user_pool_client.client.id]
  }
}

resource "aws_apigatewayv2_route" "get_BACKEND-POC" {
  api_id        = aws_apigatewayv2_api.main.id
  route_key     = "GET /allpost" // give your own endpoint name in place of allpost
  target        = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
  authorization_type    = "JWT"
  //authorization_scopes = ["openid"]  # Set the required scopes for authorization
  authorizer_id        = aws_apigatewayv2_authorizer.cognito_authorizer.id
}



resource "aws_apigatewayv2_route" "post_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /addpost" // give your own endpoint name in place of addpost
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}




resource "aws_apigatewayv2_route" "deletepost_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "DELETE /deletepostbypostid"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}


resource "aws_apigatewayv2_route" "addsignup_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /addsignup"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}


resource "aws_apigatewayv2_route" "get_token_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /get_token" // give your own endpoint name in place of allpost
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}



resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.BACKEND-POC.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

output "BACKEND-POC_base_url" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}


```


AWS API Gatewayv2 Setup with AWS Lambda Integration
This Terraform script sets up an AWS API Gatewayv2 instance with HTTP protocol type and integrates it with an AWS Lambda function. The API Gatewayv2 instance has defined routes for various HTTP methods, enabling communication between clients and the Lambda function.

Prerequisites
Before running this Terraform script, ensure you have the following:

An AWS account with appropriate permissions to create API Gatewayv2, Lambda, and CloudWatch Log Group resources.
Terraform installed locally.
AWS CLI configured with necessary credentials.
Usage
Clone this repository or download the Terraform script (main.tf) to your local environment.
Open a terminal or command prompt and navigate to the directory containing the script.
Run terraform init to initialize Terraform and download necessary providers.
Run terraform plan to review the execution plan.
Run terraform apply to create the resources as defined in the script.
Description
This Terraform script creates the following AWS resources:

### API Gatewayv2 API: Defines an HTTP protocol type API named "main".

```

resource "aws_apigatewayv2_api" "main" {
  name          = "main"  // give your own name
  protocol_type = "HTTP"
}


```

### API Gatewayv2 Stage: Creates a "dev" stage for the API with automatic deployment enabled. Also configures access logging to a specified CloudWatch Log Group with JSON formatting of log entries.

```

resource "aws_apigatewayv2_stage" "dev" {
  api_id = aws_apigatewayv2_api.main.id

  name        = "dev" // give your own name
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.main_api_gw.arn

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


```

### CloudWatch Log Group: Sets up a log group to store API Gatewayv2 access logs with a retention period of 14 days.

```
resource "aws_cloudwatch_log_group" "main_api_gw" {
  name = "/aws/api-gw/${aws_apigatewayv2_api.main.name}"

  retention_in_days = 14
}


```

### API Gatewayv2 Integration: Connects the API Gatewayv2 instance to an AWS Lambda function using an AWS_PROXY integration type and HTTP method POST.

```

resource "aws_apigatewayv2_integration" "lambda_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  integration_uri    = aws_lambda_function.BACKEND-POC.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

```

### Cognito Authorization: Configures a JWT-based authorizer for securing API endpoints.

```

resource "aws_apigatewayv2_authorizer" "cognito_authorizer" {
  api_id             = aws_apigatewayv2_api.main.id
  name               = "cognito-authorizer"
  authorizer_type    = "JWT"
  identity_sources   = ["$request.header.Authorization"]  # Assuming JWT token is in the Authorization header
  jwt_configuration {
    issuer             = "https://cognito-idp.${var.AWS_REGION}.amazonaws.com/${aws_cognito_user_pool.user_pool.id}"
    audience           = [aws_cognito_user_pool_client.client.id]
  }
}


```


### API Gatewayv2 Routes: Defines specific routes (GET /allpost and POST /addpost) mapped to the AWS Lambda integration.

```
resource "aws_apigatewayv2_route" "get_BACKEND-POC" {
  api_id        = aws_apigatewayv2_api.main.id
  route_key     = "GET /allpost" // give your own endpoint name in place of allpost
  target        = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
  authorization_type    = "JWT"
  //authorization_scopes = ["openid"]  # Set the required scopes for authorization
  authorizer_id        = aws_apigatewayv2_authorizer.cognito_authorizer.id
}



resource "aws_apigatewayv2_route" "post_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /addpost" // give your own endpoint name in place of addpost
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}




resource "aws_apigatewayv2_route" "deletepost_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "DELETE /deletepostbypostid"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}


resource "aws_apigatewayv2_route" "addsignup_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "POST /addsignup"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}


resource "aws_apigatewayv2_route" "get_token_BACKEND-POC" {
  api_id = aws_apigatewayv2_api.main.id

  route_key = "GET /get_token" // give your own endpoint name in place of allpost
  target    = "integrations/${aws_apigatewayv2_integration.lambda_BACKEND-POC.id}"
}



```

### AWS Lambda Permission: Grants permission to API Gatewayv2 to invoke the associated Lambda function.

```

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.BACKEND-POC.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

output "BACKEND-POC_base_url" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}

```

Notes
Ensure proper AWS permissions and roles are configured for the resources to function correctly.
Additional routes (e.g., DELETE and PUT) are provided as commented-out code. Uncomment and configure these routes as needed.
Outputs
BACKEND-POC_base_url: Provides the base URL of the "dev" stage for accessing the API Gatewayv2.
Cleanup
To delete the created resources:

Run terraform destroy to remove all the resources provisioned by this script.
Confirm the deletion by entering 'yes' when prompted.
Feel free to customize this README further based on your project's specific requirements and add any additional information or instructions as needed.









### Variables

- `AWS_REGION`: Specifies the AWS region for deployment.

### Resources

1. **API Gateway Setup:**
   - Creates an HTTP API named "main."
   - Establishes a "dev" stage with auto-deployment and CloudWatch logging.

2. **Cognito Authorization:**
   - Configures a JWT-based authorizer for securing API endpoints.

3. **Lambda Integration:**
   - Integrates the API with the Lambda function "BACKEND-POC" for various HTTP methods (GET, POST, DELETE).

4. **Route Configuration:**
   - Defines routes ("/allpost", "/addpost", "/deletepostbypostid", "/addsignup", "/get_token") with associated integrations and authorization.

5. **Permissions:**
   - Grants permission for API Gateway to invoke the specified Lambda function.

## Usage

1. **Clone Repository:**

2. **Initialize Terraform:**

3. **Review and Apply Changes:**

4. **Accessing API:**
- Retrieve the API base URL from the Terraform output.
- Use appropriate HTTP methods with endpoints ("/allpost", "/addpost", etc.) for testing.

## Notes

- Ensure AWS credentials are configured properly.
- Customize endpoint names, AWS region, and other configurations as needed.
- Monitor CloudWatch logs for API activity and errors.







