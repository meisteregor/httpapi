#!groovy
// Check 3.120.209.100 properties
properties([disableConcurrentBuilds()])

pipeline {
    agent { 
        label 'master'
        }
    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
        timestamps()
    }
    stages {
        stage("Prep Env") {
            steps {
                sh 'ssh root@3.120.209.100 \'yum install epel-release&&yum -y update&&yum -y install yum-utils&&yum -y groupinstall development&&yum -y install https://centos7.iuscommunity.org/ius-release.rpm&&yum -y install python35u-pip&&rm -rf ~/httpapi&&git clone https://github.com/meisteregor/httpapi\''
            }
        }
        stage("Build Egg") {
            steps {
                sh 'ssh root@3.120.209.100 \'python3.5 -m easy_install httpapi/http_api-1.0-py3.5.egg\''
            }
        }
	stage("Index DB") {
            steps {
                sh 'ssh root@3.120.209.100 \'python3.5 /usr/lib/python3.5/site-packages/MarkupSafe-1.1.0-py3.5-linux-x86_64.egg index --db index.db --data /home/ec2-user/test_data\''
            }
        }
	stage("Run app") {
            steps {
                sh 'ssh root@3.120.209.100 \'python3.5 /usr/lib/python3.5/site-packages/MarkupSafe-1.1.0-py3.5-linux-x86_64.egg service --port 5001\''
            }
        }

    }
}
