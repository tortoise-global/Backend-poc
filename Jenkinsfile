
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
                git branch: 'main', credentialsId: 'rajsekhar', url: 'https://github.com/tortoise-NRI/Backend-poc.git'
                // git branch: 'main', credentialsId: 'admin', url: 'https://github.com/tortoise-NRI/Backend-poc.git'

                // git branch: 'main', credentialsId: 'admin', url: 'https://github.com/tortoise-NRI/Backend-poc.git'
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