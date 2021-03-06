node {

    checkout scm

    stage('Test'){
        sh "echo 'testing...'"
        sh "echo 'test success'"
    }
    stage('Build Docker Image and push it to private registry') {
        def customImage = docker.build("python/simpleflaskapp","./flask")
        sh "docker tag python/simpleflaskapp localhost:5000/python/simpleflaskapp"
        sh "docker push localhost:5000/python/simpleflaskapp"

    }
    stage('Deploy Container') {
        sh "docker compose -f flask/docker-compose.yml up -d --build --remove-orphans"
        echo "Deployed successfully!!!"
    }

}
