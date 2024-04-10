
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


