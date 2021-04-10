pipeline{
    agent any


    environment{
        PROJECT_NAME = "${env.JOB_NAME}"
        REGISTRY_URL = "172.28.5.10:5000"
        REGISTRY_AUTH = credentials("my-docker-registry") // registry credentials
        HOST_IP = '172.28.5.254' // gateway of docker network points to our host
        HOST_CREDENTIALS = credentials("host")
    }
    stages{

        stage('Fetch'){
            steps{

                git branch: 'master',
                credentialsId: 'k-tsiakas@github',
                url: 'https://github.com/k-tsiakas/docker-flask.git'

                script{
                    echo "init"
                    withDockerRegistry(credentialsId:"my-docker-registry", url: "http://${env.REGISTRY_URL}"){
                        echo "Successfull login to docker registry"
                    }
                    env.BUILD_VERSION = sh(returnStdout:  true, script: "git tag --sort=-creatordate | head -n 1").trim()
                    echo "Job Name:     ${env.JOB_NAME}"
                    echo "Build Version:${env.BUILD_VERSION}"
                    env.DOCKER_IMAGE = "${env.PROJECT_NAME}"
                    echo "Docker Image: ${env.DOCKER_IMAGE}"

               }


            }
        }
        stage('Build'){ //build project in our host

            steps{

                script{
                    def remote = [:]
                    remote.name = "kt_host"
                    remote.host = "${HOST_IP}"
                    remote.allowAnyHosts = true
                    withCredentials([usernamePassword(credentialsId: 'host', passwordVariable: 'password', usernameVariable: 'userName')]) {
                          remote.user = userName
                          remote.password = password
                          def path = "/home/${HOST_CREDENTIALS_USR}/Desktop/Projects"
                          // create project dir in host
                          def init_cmd = "mkdir -p ${path}/${PROJECT_NAME}"
                          sshCommand remote: remote, command: init_cmd
                          // copy our contents within the dir
                          sshPut remote: remote, from: '.', into: path
                          // login to registry
                          def login_cmd = "docker login -u=${REGISTRY_AUTH_USR} -p=${REGISTRY_AUTH_PSW} ${REGISTRY_URL}"
                          sshCommand remote: remote, command: login_cmd
                          // build image
                          def build_cmd = "cd ${path}/${PROJECT_NAME}/ && docker build -t ${DOCKER_IMAGE}:${env.BUILD_VERSION} ."
                          sshCommand remote: remote, command: build_cmd
                          // tag image
                          def tag_cmd = "docker tag ${DOCKER_IMAGE}:${env.BUILD_VERSION} ${REGISTRY_URL}/${DOCKER_IMAGE}:${env.BUILD_VERSION}"
                          sshCommand remote: remote, command: tag_cmd
                          // push image to registry
                          def push_cmd = "docker push ${REGISTRY_URL}/${DOCKER_IMAGE}:${env.BUILD_VERSION}"
                          sshCommand remote: remote, command: push_cmd
                    }
                }

            }
        }
        stage('Test'){ //test project in our host

            steps{

                script{
                    def remote = [:]
                    remote.name = "kt_host"
                    remote.host = "${HOST_IP}"
                    remote.allowAnyHosts = true
                    withCredentials([usernamePassword(credentialsId: 'host', passwordVariable: 'password', usernameVariable: 'userName')]) {
                          remote.user = userName
                          remote.password = password
                          //echo test
                          def test_cmd = "echo 'hello... just testing' > /home/${HOST_CREDENTIALS_USR}/Desktop/Projects/${PROJECT_NAME}/test.txt"
                          sshCommand remote: remote, command: test_cmd

                    }
                }

            }
        }
        stage('Deploy'){ //deploy project in our host

            steps{

                script{
                    def remote = [:]
                    remote.name = "kt_host"
                    remote.host = "${HOST_IP}"
                    remote.allowAnyHosts = true
                    withCredentials([usernamePassword(credentialsId: 'host', passwordVariable: 'password', usernameVariable: 'userName')]) {
                          remote.user = userName
                          remote.password = password
                          // stop existing container
                          def stop_cmd = "cd /home/${HOST_CREDENTIALS_USR}/Desktop/Projects/${PROJECT_NAME}/ && docker-compose down"
                          sshCommand remote: remote, command: stop_cmd
                          //remove image from host so we can check the registry
                          def delete_cmd = "docker rmi ${DOCKER_IMAGE}:${env.BUILD_VERSION}"
                          sshCommand remote: remote, command: delete_cmd
                          // pull image from registry
                          def pull_cmd = "docker pull ${REGISTRY_URL}/${DOCKER_IMAGE}:${env.BUILD_VERSION}"
                          sshCommand remote: remote, command: pull_cmd
                          // run new container
                          def deploy_cmd = "cd /home/${HOST_CREDENTIALS_USR}/Desktop/Projects/${PROJECT_NAME}/ && docker-compose up -d --build --remove-orphans"
                          sshCommand remote: remote, command: deploy_cmd
                    }
                }

            }
        }
    }
}
