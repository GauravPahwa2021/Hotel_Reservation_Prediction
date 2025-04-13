pipeline {
    agent any

    stages {
        stage('cloning github repo to jenkins workspace') {
            steps {
                script {
                    echo 'checkout gtihub repository'
                    // Add your build commands here
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/GauravPahwa2021/Hotel_Reservation_Prediction.git']])
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