pipeline {
    agent any

    stages {
        stage("Smoke Test") {
            steps {
                script {
                        sh """
                                file='MyCSV.csv'
                                success=\$(head -1 \$file | tr ',' '\n' | nl |grep -w "success" | tr -d " " | awk -F " " '{print \$1}')
                                url=$(head -1 \$file | tr ',' '\n' | nl |grep -w "URL" | tr -d " " | awk -F " " '{print \$1}')
                                responseCode=\$(head -1 \$file | tr ',' '\n' | nl |grep -w "responseCode" | tr -d " " | awk -F " " '{print \$1}')
                                responseMessage=\$(head -1 \$file | tr ',' '\n' | nl |grep -w "responseMessage" | tr -d " " | awk -F " " '{print \$1}')
                                failureMessage=\$(head -1 \$file | tr ',' '\n' | nl |grep -w "failureMessage" | tr -d " " | awk -F " " '{print \$1}')

                                #echo"$(head -1 $file | tr ',' '\n' | nl |grep -w "success" | tr -d " " | awk -F " " '{print $1}')"
                                while IFS="," read -r rec1 rec2 rec3 rec4 rec5; do
                                # do something... Don't forget to skip the header line!
                                if [[ $rec1 != 200 ]]
                                then
                                    echo \$rec1 \$rec2 \$rec3 \$rec4 \$rec5
                                fi
                                done < <(cut -d "," -f\${success},${url},\${responseCode},\${responseMessage},\${failureMessage} $file | tail -n +2)
                    } 
                }
            }  
        }
}
