
pipeline {

    environment {
        AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        SUDO_PASSWORD = credentials('SUDO_PASSWORD') 

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

                    def sudoPassword = credentials('SUDO_PASSWORD')
                    if (sudoPassword) {
                        def command = "echo ${sudoPassword} | sudo -S apt-get update"
                        def proc = command.execute()
                        proc.waitFor()

                        if (proc.exitValue() == 0) {
                            command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
                            proc = command.execute()
                            proc.waitFor()
                        } 
                        else {
                        echo "Failed to install dependencies"
                        }   
                        if (proc.exitValue() == 0) {
                            command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
                            proc = command.execute()
                            proc.waitFor()
                        } 
                        else {
                        echo "Failed to install dependencies"
                        }  

                        if (proc.exitValue() == 0) {
                            command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
                            proc = command.execute()
                            proc.waitFor()
                        } 
                        else {
                        echo "Failed to install dependencies"
                        }  
                        
                        if (proc.exitValue() == 0) {
                            command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
                            proc = command.execute()
                            proc.waitFor()
                        } 
                        else {
                        echo "Failed to install dependencies"
                        }  

                        if (proc.exitValue() == 0) {
                            command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
                            proc = command.execute()
                            proc.waitFor()
                        } 
                        else {
                        echo "Failed to install dependencies"
                        } 

                        
                    }
                   else {
                    echo "No sudo password provided"
                
        


                    // sh '''
                    //     echo "${sudoPassword}" | sudo -S apt-get update
                    //     echo "${sudoPassword}" | sudo -S apt-get install -y python3 python3-pip zip
                    //     echo "${sudoPassword}" | sudo -S rm -rf python
                    //     echo "${sudoPassword}" | sudo -S mkdir python
                    //     echo "${sudoPassword}" | sudo -S pip3 install -r requirements.txt -t python/
                    //     echo "${sudoPassword}" | sudo -S zip -r python.zip python/
                    // '''
                    // withCredentials([string(credentialsId: 'SUDO_PASSWORD', variable: 'SUDO_PASS')]) {
                    //     sh '''
                    //         sudo -S apt-get update <<< "$SUDO_PASS"
                    //         sudo -S apt install python3 python3-pip zip -y <<< "$SUDO_PASS"
                    //         sudo -S rm -rf python <<< "$SUDO_PASS"
                    //         sudo -S mkdir python <<< "$SUDO_PASS"
                    //         sudo -S pip3 install -r requirements.txt -t python/ <<< "$SUDO_PASS"
                    //         sudo -S zip -r python.zip python/ <<< "$SUDO_PASS"
                    //     '''
                    // }
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