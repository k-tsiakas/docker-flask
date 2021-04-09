pipeline{
    agent any
    environment{
        PROJECT_NAME = "${env.JOB_NAME}"
        REGISTRY_URL = "172.28.5.10:5000"
        REGISTRY_AUTH = credentials("my-docker-registry") // credentials για το registry μας
        BUILD_VERSION = sh(returnStdout:  true, script: "git tag --sort=-creatordate | head -n 1").trim() // παιρνουμε το τελευταιο tag του repository
        GATEWAY = "172.28.5.254" // gateway of docker network points to our host
        // HOST_CREDENTIALS = credentials("host_credentials") // credentials για το host μας
        DOCKER_IMAGE = "${env.PROJECT_NAME}:${BUILD_VERSION}"

    }
    stages{
        stage('Initialize Environment'){
            steps{
                script{
                    echo "init"
                    withDockerRegistry(credentialsId:"my-docker-registry", url: "${env.GETEWAY}:5000"){
                        echo "ok"
                    }
                    withDockerRegistry(credentialsId:"my-docker-registry", url: "${env.REGISTRY_URL}"){
                        echo "ok"
                    }
                    echo "${env.JOB_NAME}"
               }

            }
        }
    }
}
