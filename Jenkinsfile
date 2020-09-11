pipeline {
    agent { docker { image 'python:3.7.2' } }
    withEnv(["HOME=${env.WORKSPACE}"]) {
        stages {
            stage('build') {
                steps {
                    sh 'pip install flask'
                    sh 'pip list'
                }
            }
            stage('test') {
                steps {
                    sh 'python test.py'
                }
            }
        }
    }
}
