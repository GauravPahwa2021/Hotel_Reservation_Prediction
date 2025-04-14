pipeline {
    agent any

     environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('cloning github repo to jenkins workspace') {
            steps {
                script {
                    echo 'checkout gtihub repository............'
                    // Add your build commands here
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/GauravPahwa2021/Hotel_Reservation_Prediction.git']])
                }
            }
        }
    }

    stages {
        stage('Setting up our Virtual Environment and Installing dependancies') {
            steps {
                script {
                    echo 'creating virtual environment and installing dependencies..............'
                    // Add your build commands here
                    sh '''  
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Clean up workspace after the build
        }
    }
}