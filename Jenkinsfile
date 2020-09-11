pipeline {
    agent { docker { image 'python:3.7.2' } }
    stages {
        stage('build') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install Pillow --user'
                    sh 'pip install flask'
                    sh 'pip list'
                    sh 'mkdir /app'
                    sh 'wget https://github.com/fergusmclellan/image_creator/raw/master/cour.ttf -O /app/cour.ttf'
                }
            }
        }
        stage('test') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'python test.py'
                }
            }
        }
    }
}
