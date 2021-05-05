pipeline {
    agent any

    stages {
        stage("Smoke Test") {
            steps {
                script {
                        stage("Running tests on") {  
                           sh(script: 'pip install -r requirements.txt') 
                            def respose = sh(script: 'python get_version_numbers.py', returnStdout: true)
                            echo response
                                }

                        }  
                        }
                    } 
                }
            }  
        }
}
