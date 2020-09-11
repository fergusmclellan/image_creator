pipeline {
    agent { /usr/local/bin/docker { image 'python:3.7.2' } }
    stages {
        stage('build') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install flask'
                }
            }
        }
        stage('test') {
            steps {
                sh 'python test.py'
            }
        }
    }
}
