def sendNotification(Map params) {
    dir('smoke-test') {
        sh(script: """
        python send_reposnse_to_teams.py failed_results.csv ${env.BUILD_URL} ${params.statusResult}
        rm -f failed_results.csv
        """) 
    }
}
def publishResult(def webapp) {
    try{
        echo "************************************************** Publish perfomance result **************************************************"
        perfReport errorFailedThreshold: 0, 
        errorUnstableThreshold: 0, 
        filterRegex: '', 
        relativeFailedThresholdNegative: 0.0, 
        relativeFailedThresholdPositive: 0.0, 
        relativeUnstableThresholdNegative: 0.0, 
        relativeUnstableThresholdPositive: 0.0, 
        sourceDataFiles: "**/${webapp}*.jtl"
        sh "**/checkStatus.sh **/${webapp}*.jtl"
    }
    catch(ex) {
        result = 'Fail'
        currentBuild.result = 'UNSTABLE'
        echo "****************************************************************************************************"
        return "Failed"
    }
    echo "****************************************************************************************************"
    return "Success"
}
pipeline {
    agent any
    environment {
         WEBAPP_CRED = credentials('webapps')
    }
    stages {
        stage("Install dependencies") {
            steps {
                dir('smoke-test') {
                    echo "************************************************** Install packages **************************************************"
                    sh("""
                    rm -rf failed_results.csv
                    pip install -r requirements.txt
                    """)
                    echo "***********************************************************************************************************************"
                }
            }
        }
        stage("Smoke Test") {
            steps {
                script {
                    def webappConfig = readYaml file: "smoke-test/webapp.yml"
                    webapps = webappConfig.webapp
                    for(String webapp:webapps) {
                        stage("Running tests on ${webapp}") {   
                            catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                                dir('smoke-test') {
                                    echo "************************************************** Run test on : ${webapp} **************************************************"
                                    sh """
                                    rm -rf **/*.jtl **/jmeter.log
                                    host=${webapp}
                                    username=${WEBAPP_CRED_USR}              
                                    [ -f  \$host.jmx ] && fille='\$host.jmx' || file='test-case.jmx'
                                    password=\$(python3 encrypt_password.py ${WEBAPP_CRED_PSW} https://${webapp})
    
                                    jmeter -n -t \$file -Jhost=\$host  -Jusername=\$username -Jpassword=\$password  -f -l ${webapp}-testresult.jtl
                                    """
                                    echo "*******************************************************************************************************************************"
                                
                                    sh(script: """
                                    python generate_failed_reposnse.py ${webapp}-testresult.jtl failed_results.csv
                                    """
                                    ) 
                                }
                                def report = publishResult(webapp)
                                if(report == 'Failed') {
                                    sh "exit 1"
                                }
                            }
                        }  
                    }
                }
            }
        }
    }
    post {
        success {
            sendNotification(statusResult: 'success')
        }
        unstable {
           sendNotification(statusResult: 'unstable')
        }
        failure {
            sendNotification(statusResult: 'failure')
        }
    }
}
