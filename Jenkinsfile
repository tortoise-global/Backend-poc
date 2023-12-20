
pipeline {

    environment {
        AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        //SUDO_PASSWORD = credentials('SUDO_PASSWORD') 

    }

   agent  any
     stages {
        stage ("checkout from GIT") {
            steps {
                //git branch: 'main', credentialsId: 'rajsekhar', url: 'https://github.com/tortoise-NRI/Backend-poc.git'
                git branch: 'main', credentialsId: 'admin', url: 'https://github.com/tortoise-NRI/Backend-poc.git'
            }
        }

        stage("Install Python dependencies and create zip") {
            steps {
                // withCredentials([string(credentialsId: 'SUDO_PASSWORD', variable: 'SUDO_PASS')]) {
                    script {

                        // sh "echo ${SUDO_PASS} | sudo -S whoami"

                        //sh "echo iconsoftware@8421 | sudo -S whoami"
                        // sudo_pass : "iconsoftware@8421"

                        // echo "SUDO_PASS: ${SUDO_PASS}"
                        // sh "echo ${sudo_pass} | sudo -S whoami"
                        // def hardcodedPassword = "iconsoftware@8421"
                        //     echo "SUDO_PASS: ${hardcodedPassword}"
                        //     sh "echo ${hardcodedPassword} | sudo -S whoami"

                            // sh "whoami"
                         
                            // sh "su - ubuntu"
                            // sh "python"


                            // sh "whoami"

                            // sh 'echo "python" | su - ubuntu -c "whoami"'

                            // sh "apt-get updat"

                            // sh '''
                            //     expect -c '
                            //         spawn su - ubuntu
                            //         expect "Password:"
                            //         send "python\\r"
                            //         interact
                            //     '
                            // '''

                            sh "whoami"



                        // sh  '''
                        //     sudo apt-get update
                        //     sudo apt-get install -y python3 python3-pip zip
                        //     sudo -rf python
                        //     sudo mkdir python
                        //     sudo pip3 install -r requirements.txt -t python/
                        //     sudo zip -r python.zip python/
                        // '''

                    }
                    }
                    }
                    // }
        //                 // def sudoPassword = env.SUDO_PASS

        //                 // sh "echo ${sudoPassword} | sudo -S apt-get update"
        //                 // sh "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
        //                 // sh "echo ${sudoPassword} | sudo -S rm -rf python"
        //                 // sh "echo ${sudoPassword} | sudo -S mkdir python"
        //                 // sh "echo ${sudoPassword} | sudo -S pip3 install -r requirements.txt -t python/"
        //                 // sh "echo ${sudoPassword} | sudo -S zip -r python.zip python/"
                    
        //             }
        //         //     def sudoPassword = credentials('SUDO_PASSWORD')
        //         //     if (sudoPassword) {
        //         //         def command = "echo ${sudoPassword} | sudo -S apt-get update"
        //         //         def proc = command.execute()
        //         //         proc.waitFor()

        //         //         if (proc.exitValue() == 0) {
        //         //             command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
        //         //             proc = command.execute()
        //         //             proc.waitFor()
        //         //         } 
        //         //         else {
        //         //         echo "Failed to install dependencies"
        //         //         }   
        //         //         if (proc.exitValue() == 0) {
        //         //             command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
        //         //             proc = command.execute()
        //         //             proc.waitFor()
        //         //         } 
        //         //         else {
        //         //         echo "Failed to install dependencies"
        //         //         }  

        //         //         if (proc.exitValue() == 0) {
        //         //             command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
        //         //             proc = command.execute()
        //         //             proc.waitFor()
        //         //         } 
        //         //         else {
        //         //         echo "Failed to install dependencies"
        //         //         }  
                        
        //         //         if (proc.exitValue() == 0) {
        //         //             command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
        //         //             proc = command.execute()
        //         //             proc.waitFor()
        //         //         } 
        //         //         else {
        //         //         echo "Failed to install dependencies"
        //         //         }  

        //         //         if (proc.exitValue() == 0) {
        //         //             command = "echo ${sudoPassword} | sudo -S apt-get install -y python3 python3-pip zip"
        //         //             proc = command.execute()
        //         //             proc.waitFor()
        //         //         } 
        //         //         else {
        //         //         echo "Failed to install dependencies"
        //         //         } 

                        
        //         //     }
        //         //    else {
        //         //     echo "No sudo password provided" 
        //         //     }


        //             // sh '''
        //             //     echo "${sudoPassword}" | sudo -S apt-get update
        //             //     echo "${sudoPassword}" | sudo -S apt-get install -y python3 python3-pip zip
        //             //     echo "${sudoPassword}" | sudo -S rm -rf python
        //             //     echo "${sudoPassword}" | sudo -S mkdir python
        //             //     echo "${sudoPassword}" | sudo -S pip3 install -r requirements.txt -t python/
        //             //     echo "${sudoPassword}" | sudo -S zip -r python.zip python/
        //             // '''
        //             // withCredentials([string(credentialsId: 'SUDO_PASSWORD', variable: 'SUDO_PASS')]) {
        //             //     sh '''
        //             //         sudo -S apt-get update <<< "$SUDO_PASS"
        //             //         sudo -S apt install python3 python3-pip zip -y <<< "$SUDO_PASS"
        //             //         sudo -S rm -rf python <<< "$SUDO_PASS"
        //             //         sudo -S mkdir python <<< "$SUDO_PASS"
        //             //         sudo -S pip3 install -r requirements.txt -t python/ <<< "$SUDO_PASS"
        //             //         sudo -S zip -r python.zip python/ <<< "$SUDO_PASS"
        //             //     '''
        //             // }
        //         }
        //     }
        // }



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