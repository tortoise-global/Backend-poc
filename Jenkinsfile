pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        SUDO_PASSWORD = 'turtil' // Replace with actual sudo password
    }

    stages {
        stage("checkout from GIT") {
            steps {
                git branch: 'main', credentialsId: 'rajsekhar', url: 'https://github.com/tortoise-NRI/Backend-poc.git'
            }
        }

        stage("Install Python dependencies and create zip") {
            steps {
                script {
                    // Assuming requirements.txt exists in the checked out directory
                    // sh 'sudo -n apt-get update'
                    // sh 'sudo -n apt install python3 python3-pip zip -y'
                    // sh 'sudo -n rm -rf python'
                    // sh 'sudo -n mkdir python'
                    // sh 'sudo -n pip3 install -r requirements.txt -t python/'
                    // sh 'sudo -n zip -r python.zip python/'

                    sh 'sudo -S apt-get update <<< $SUDO_PASSWORD'
                    sh 'sudo -S apt install python3 python3-pip zip -y <<< $SUDO_PASSWORD'
                    sh 'sudo -S rm -rf python <<< $SUDO_PASSWORD'
                    sh 'sudo -S mkdir python <<< $SUDO_PASSWORD'
                    sh 'sudo -S pip3 install -r requirements.txt -t python/ <<< $SUDO_PASSWORD'
                    sh 'sudo -S zip -r python.zip python/ <<< $SUDO_PASSWORD'
                }
            }
        }

        stage("terraform init") {
            steps {
                sh 'terraform init'
            }
        }

        stage("terraform fmt") {
            steps {
                sh 'terraform fmt'
            }
        }

        stage("terraform validate") {
            steps {
                sh 'terraform validate'
            }
        }

        stage("terraform plan") {
            steps {
                sh 'terraform plan'
            }
        }

        stage("terraform apply") {
            steps {
                sh 'terraform apply --auto-approve'
            }
        }
    }
}
