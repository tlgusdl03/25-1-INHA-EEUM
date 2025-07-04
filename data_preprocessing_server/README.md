# MQTT_server

## 프로젝트 개요
- 파이썬 기반의 FastAPI 서버 MQTT_Client를 사용, IoT 센서로 부터 수집한 데이터에 대해, 전처리, DB 저장을 수행하고, 사용자 요청에 따라 필요한 데이터를 제공하는 역할을 수행한다.

## 프로젝트 구조

```
data_server
├─ database                       // 로컬 테스트 용 database init 파일
├─ docker-compose.yml             // 로컬 테스트 용 인프라 및 서버 구축 파일
├─ Dockerfile                     // /src 폴더 빌드용 dockerfile
├─ Jenkinsfile                    // 클라우드 배포용 Jenkinsfile
├─ mosquitto                      // 로컬 테스트 용 메시지 브로커 설정 파일
│  └─ config
│     └─ mosquitto.conf
├─ README.md
├─ requirements.txt               // 필요 의존성 파일
├─ src                            // 서비스 코드 
│  ├─ database.py
│  ├─ main.py
│  ├─ models.py
│  └─ mqtt_client.py
└─ test                           // 테스트 코드
   └─ test_mqtt_integration.py    
```

## 배포 과정

<img src="https://github.com/user-attachments/assets/539a4eb7-c50e-4856-93b4-517da36751d7" width="700" height="350">

1. github Action으로 코드 테스트 및 docker image 빌드, ecr로 push

```
name: CI to CD (build + direct Jenkins trigger)

on:
push:
branches: ["main"]
paths-ignore: - Jenkinsfile - docker-compose.yml

jobs:
build-and-deploy:
runs-on: ubuntu-latest

    steps:
      - name: checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest test/

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-northeast-2

      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push Docker image to ECR
        env:
          ECR_REGISTRY: ${{ secrets.ECR_REGISTRY }}
          ECR_REPOSITORY: ${{ secrets.ECR_REPOSITORY }}
          IMAGE_NAME: data_server
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:${{ github.sha }} .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:${{ github.sha }}
          docker tag $ECR_REGISTRY/$ECR_REPOSITORY:${{ github.sha }} $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

```

2. Jenkins로 이미지 pull 하여 docker compose로 실행

```
pipeline {
  agent any

  environment {
    IMAGE_NAME = "data_server"
  }

  stages {
    stage('Clone') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[
            url: 'https://github.com/25-1-INHA-EEUM/data_server.git',
            credentialsId: 'github-token'
          ]]
        ])
      }
    }

    stage('Deploy to Target EC2') {
      steps {
        withCredentials([
          string(credentialsId: 'target-host-ip', variable: 'TARGET_HOST_SECRET'),
          string(credentialsId: 'ecr-registry', variable: 'ECR_REGISTRY_SECRET')
        ]) {
          withEnv(["TARGET_HOST=${env.TARGET_HOST_SECRET}", "ECR_REGISTRY=${env.ECR_REGISTRY_SECRET}"]) {
            sshagent(credentials: ['data-server-ec2-key']) {

              sh """
                echo "📦 docker-compose.yml 전송 중..."
                ssh -o StrictHostKeyChecking=no ec2-user@${env.TARGET_HOST} "
                  sudo rm -rf ~/data_server &&
                  mkdir -p ~/data_server &&
                  sudo chown ec2-user:ec2-user ~/data_server
                "
                scp -r -o StrictHostKeyChecking=no docker-compose.yml ec2-user@${env.TARGET_HOST}:~/data_server/
              """

              sh """
                echo "🛠️ Amazon Linux 2023용 docker, aws-cli, docker composeV2 설치..."
                ssh -o StrictHostKeyChecking=no ec2-user@${env.TARGET_HOST} "
                  sudo yum update -y &&
                  sudo yum install -y docker aws-cli &&
                  sudo systemctl enable --now docker &&
                  sudo mkdir -p ~/.docker/cli-plugins &&
                  sudo curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose &&
                  sudo chmod +x ~/.docker/cli-plugins/docker-compose
                "
              """

              sh """
                echo "🚀 배포 시작 (ECR Pull + Clean Deploy)..."
                ssh -o StrictHostKeyChecking=no ec2-user@${env.TARGET_HOST} "
                  aws ecr get-login-password --region ap-northeast-2 | sudo docker login --username AWS --password-stdin ${env.ECR_REGISTRY} &&
                  sudo docker pull ${env.ECR_REGISTRY}/${env.IMAGE_NAME}:latest &&
                  cd ~/data_server &&
                  sudo docker-compose down &&
                  sudo docker image prune -af &&
                  sudo docker-compose up -d
                "
              """
            }
          }
        }
      }
    }
  }
}
```

- 배포 성공 화면(/docs 접속 화면)
  <img src="https://github.com/user-attachments/assets/f8297bd0-e609-4d0e-8e47-02d88de4b0ca" width="700" height="350">

## 중간 테스트 결과

- mqtt 메시지 저장

```

받은 메시지: {'sensor_id': 'sensor01', 'temperature': 25.5, 'humidity': 55.0, 'tvoc': 0.4, 'noise': 30.2}

2025-04-23 09:06:26,269 INFO sqlalchemy.engine.Engine BEGIN (implicit)

2025-04-23 09:06:26,271 INFO sqlalchemy.engine.Engine INSERT INTO readings (sensor_id, ts, temperature, humidity, tvoc, noise) VALUES ($1::VARCHAR, $2::TIMESTAMP WITH TIME ZONE, $3::FLOAT, $4::FLOAT, $5::FLOAT, $6::FLOAT)

2025-04-23 09:06:26,271 INFO sqlalchemy.engine.Engine [cached since 516s ago] ('sensor01', datetime.datetime(2025, 4, 23, 9, 6, 26, 268162), 25.5, 55.0, 0.4, 30.2)

2025-04-23 09:06:26,274 INFO sqlalchemy.engine.Engine COMMIT

✅ DB 저장 완료

```

- test_mqtt_integration.py 테스트 결과 (메시지 브로커로 메시지를 저장한 후 db에 직접 연결하여 같은 데이터가 저장되어있는지 확인함)
```
[Running] python -u "c:\project-workspace\25-1-jongsul\data_server\test\test_mqtt_integration.py"
Python executable: C:\Users\tlgus\AppData\Local\Programs\Python\Python311\python.exe
데이터 세팅 완료
MQTT 메시지 전송 완료
DB에서 조회된 값: (1, Decimal('25.50'), Decimal('55.00'), Decimal('0.40'), Decimal('30.20'), Decimal('10.50'), Decimal('5.30'))
✅ 테스트 성공: MQTT → FastAPI → TimescaleDB 저장 정상 작동

[Done] exited with code=0 in 2.234 seconds
```

- db 조회

```2025-04-23 09:08:46,535 INFO sqlalchemy.engine.Engine BEGIN (implicit)


2025-04-23 09:08:46,540 INFO sqlalchemy.engine.Engine SELECT sensors.id, sensors.name, sensors.location


FROM sensors


2025-04-23 09:08:46,540 INFO sqlalchemy.engine.Engine [generated in 0.00054s] ()


2025-04-23 09:08:46,550 INFO sqlalchemy.engine.Engine ROLLBACK


INFO: 172.18.0.1:44972 - "GET / HTTP/1.1" 200 OK
```



```
data_server
├─ database
│  ├─ 1_init.sql
│  ├─ 2_insert_locations.sql
│  ├─ 3_insert_iot_devices.sql
│  ├─ 4_insert_sensors.sql
│  └─ 5_insert_sensor_datas.sql
├─ docker-compose.yml
├─ Dockerfile
├─ Jenkinsfile
├─ mosquitto
│  └─ config
│     └─ mosquitto.conf
├─ README.md
├─ requirements.txt
├─ src
│  ├─ database.py
│  ├─ main.py
│  ├─ models.py
│  ├─ mqtt_client.py
│  ├─ preprocessors
│  │  ├─ missing_handler.py
│  │  └─ outlier_handler.py
│  └─ validators
│     └─ sensor_data_validator.py
└─ test
   ├─ data_preprocess_test.py
   └─ test_mqtt_integration.py

```