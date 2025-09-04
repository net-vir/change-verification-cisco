pipeline {
    agent any

    parameters {
        string(name: 'USERNAME', description: 'Device login username')
        password(name: 'PASSWORD', description: 'Device login password')
        string(name: 'CHANGE_ID', description: 'Change ID for tracking')
        choice(name: 'CHANGE_TYPE', choices: ['PRE', 'POST'], description: 'Type of Change')
        file(name: 'INPUT_CSV', description: 'Upload CSV file with device IPs and commands')
    }

    environment {
        PYTHON = 'python3'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/net-vir/change-verification-cisco.git'
            }
        }

        stage('Prepare Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    mkdir -p input output
                '''
            }
        }

        stage('Handle Input CSV') {
            steps {
                sh "cp ${params.INPUT_CSV} input.csv"
            }
        }

        stage('Run Script') {
            steps {
                script {
                    // Build dynamic output filename
                    def outFile = "output/${params.CHANGE_TYPE}_${params.CHANGE_ID}.txt"
                    
                    sh """
                        . venv/bin/activate && \
                        ${env.PYTHON} your_script.py \
                        --csv input/devices.csv \
                        --username ${params.USERNAME} \
                        --password ${params.PASSWORD} \
                        --change_id ${params.CHANGE_ID} \
                        --change_type ${params.CHANGE_TYPE} \
                        --output ${outFile}
                    """
                }
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'output/*', fingerprint: true
            }
        }
    }
}
