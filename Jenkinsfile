
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



// pipeline {

//     environment {
//         AWS_ACCESS_KEY_ID     = credentials('AWS_ACCESS_KEY_ID')
//         AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
//     }

//     agent any

//     stages {
//         stage ("Checkout from Git") {
//             steps {
//                 git branch: 'main', credentialsId: 'rajsekhar', url: 'https://github.com/tortoise-NRI/Backend-poc.git'
//             }
//         }

//         stage ("Check for changes in requirements.txt") {
//             steps {
//                 script {
//                     def hasChanges = false
//                     // Check if there are changes in requirements.txt using git diff
//                     def gitDiff = sh(script: 'git diff --name-only HEAD HEAD^ | grep requirements.txt', returnStdout: true).trim()
//                     if (gitDiff != '') {
//                         hasChanges = true
//                     }

//                     // Execute the stage to install Python dependencies and create zip only if there are changes
//                     if (hasChanges) {
//                         stage("Install Python dependencies and create zip") {
//                             steps {
//                                 script {
//                                     sh  '''
//                                         sudo apt-get update
//                                         sudo apt-get install -y python3 python3-pip zip
//                                         sudo rm -rf python
//                                         sudo mkdir python
//                                         sudo pip3 install -r requirements.txt -t python/
//                                         sudo zip -r python.zip python/
//                                     '''
//                                 }
//                             }
//                         }
//                     } else {
//                         echo "No changes in requirements.txt. Skipping stage."
//                     }
//                 }
//             }
//         }

//         // Add your Terraform stages here...

//         stage ("Terraform Init") {
//             steps {
//                 sh 'terraform init'
//             }
//         }
        
//         stage ("Terraform Format") {
//             steps {
//                 sh 'terraform fmt'
//             }
//         }
        
//         stage ("Terraform Validate") {
//             steps {
//                 sh 'terraform validate'
//             }
//         }
        
//         stage ("Terraform Plan") {
//             steps {
//                 sh 'terraform plan'
//             }
//         }
        
//         stage ("Terraform Apply") {
//             steps {
//                 sh 'terraform apply --auto-approve'
//             }
//         }
//     }
// }
