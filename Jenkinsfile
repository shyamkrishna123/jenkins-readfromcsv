def webapps = readYaml file: "webapp.yml"
def jmResult = new LinkedHashMap()


pipeline {
    agent any

    stages {
        stage("Smoke Test") {
            steps {
                script {
                    for(String webapp:webapps) {
                        stage("Running tests on ${webapp}") {   
                            dir ('FolderWhereCSVIsClonedFromGit') {
                            if (fileExists('MyCSV.csv')) {
                                echo ' MyCSV.csv found'

                            readFile("MyCSV.csv").eachLine { line, count ->
                                def fields = line.split(',')
                                for(String item: fields) {
                                    println item
                                    println ' you are parsing line : ' + count
                                }
                                nodes["line${count}"] = {
                                    node {
                                        echo fields[0] + ': ' + fields[1] + ': ' + fields[2] + ': ' + fields[3] + ': ' + fields[4];
                                    }
                                }
                    }
                    } else {
                        echo ' Machines.csv Not found. Failing.'
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
            sendNotification(jmeterResult: jmResult, statusResult: 'success')
        }
        unstable {
           sendNotification(jmeterResult: jmResult, statusResult: 'unstable')
        }
        failure {
            sendNotification(jmeterResult: jmResult, statusResult: 'failure')
        }
    }
}
