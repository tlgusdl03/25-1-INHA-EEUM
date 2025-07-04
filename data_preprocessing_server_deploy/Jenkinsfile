pipeline {
  agent any

  stages {
    stage('Upload Infra to S3') {
      steps {
        withCredentials([
          string(credentialsId: 's3-bucket', variable: 'S3_BUCKET'),
          string(credentialsId: 's3-path-data-server', variable: 'S3_PATH'),
        ]) {
          sh """
            aws s3 cp docker-compose.yml s3://${S3_BUCKET}/${S3_PATH}/docker-compose.yml
            aws s3 cp --recursive database s3://${S3_BUCKET}/${S3_PATH}/database
            aws s3 cp --recursive mosquitto s3://${S3_BUCKET}/${S3_PATH}/mosquitto
          """
        }
      }
    }

    stage('Deploy via SSM') {
      steps {
        withCredentials([
          string(credentialsId: 's3-bucket', variable: 'S3_BUCKET'),
          string(credentialsId: 's3-path-data-server', variable: 'S3_PATH'),
          string(credentialsId: 'region', variable: 'REGION'),
          string(credentialsId: 'data-server-instance-id', variable: 'TARGET_INSTANCE_ID'),
          string(credentialsId: 'ecr-registry', variable: 'ECR_REGISTRY_SECRET'),
          string(credentialsId: 'postgres-user', variable: 'POSTGRES_USER_SECRET'),
          string(credentialsId: 'postgres-password', variable: 'POSTGRES_PASSWORD_SECRET'),
          string(credentialsId: 'postgres-db', variable: 'POSTGRES_DB_SECRET')
        ]) {
          sh """
          aws ssm send-command \\
            --instance-ids ${env.TARGET_INSTANCE_ID} \\
            --document-name "AWS-RunShellScript" \\
            --parameters 'commands=[
              "sudo yum update -y",
              "sudo yum install -y docker aws-cli",
              "sudo systemctl enable --now docker",
              "sudo mkdir -p /usr/local/lib/docker/cli-plugins",
              "sudo curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose",
              "sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose",
              "docker compose version",
              "mkdir -p ~/infra-deploy",
              "aws s3 cp s3://${S3_BUCKET}/${S3_PATH}/docker-compose.yml ~/infra-deploy/docker-compose.yml",
              "aws s3 cp --recursive s3://${S3_BUCKET}/${S3_PATH}/database ~/infra-deploy/database",
              "aws s3 cp --recursive s3://${S3_BUCKET}/${S3_PATH}/mosquitto ~/infra-deploy/mosquitto",
              "cd ~/infra-deploy",
              "echo POSTGRES_USER=${env.POSTGRES_USER_SECRET} > .env",
              "echo POSTGRES_PASSWORD=${env.POSTGRES_PASSWORD_SECRET} >> .env",
              "echo POSTGRES_DB=${env.POSTGRES_DB_SECRET} >> .env",
              "echo ECR_REGISTRY=${env.ECR_REGISTRY_SECRET} >> .env",
              "aws ecr get-login-password --region ${env.REGION} | docker login --username AWS --password-stdin ${env.ECR_REGISTRY_SECRET}",
              "docker compose down -v|| true",
              "docker system prune -af",
              "docker compose up -d"
            ]' \\
            --region ${env.REGION}
          """
        }
      }
    }
  }
}
