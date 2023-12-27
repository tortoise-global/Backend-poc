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


