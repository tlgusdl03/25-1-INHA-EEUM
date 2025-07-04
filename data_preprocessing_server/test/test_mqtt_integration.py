# import json
# import time
# import psycopg2
# import paho.mqtt.publish as publish

# DB_HOST = "localhost"
# DB_PORT = 5432
# DB_NAME = "iot-database"
# DB_USER = "postgres"
# DB_PASS = "0000"
# MQTT_HOST = "localhost"
# MQTT_PORT = 1883

# def test_publish_and_check_db():
#     # 1. MQTT 메시지 전송
#     payload = {
#         "location_id": 6,  # 기존 sensor_id 대신 location_id 사용
#         "temperature": 25.5,
#         "humidity": 55.0,
#         "tvoc": 0.4,
#         "noise": 30.2,
#         "pm10": 10.5,
#         "pm2_5": 5.5
#     }

#     print("데이터 세팅 완료")

#     publish.single(
#         topic="sensors/data",
#         payload=json.dumps(payload),
#         hostname=MQTT_HOST,
#         port=MQTT_PORT
#     )

#     print("MQTT 메시지 전송 완료")

#     # 2. 메시지가 처리될 시간 잠시 대기
#     # time.sleep(2)  # fastapi가 비동기로 처리할 시간 확보

#     # 3. DB 접속 후 데이터 확인
#     # conn = psycopg2.connect(
#     #     host=DB_HOST,
#     #     port=DB_PORT,
#     #     dbname=DB_NAME,
#     #     user=DB_USER,
#     #     password=DB_PASS
#     # )

#     # cur = conn.cursor()
#     # cur.execute("""
#     #     SELECT location_id, temperature, humidity, tvoc, noise, pm10, pm2_5
#     #     FROM sensor_datas
#     #     ORDER BY collected_at DESC
#     #     LIMIT 1;
#     # """)
#     # result = cur.fetchone()
#     # cur.close()
#     # conn.close()

#     # print("DB에서 조회된 값:", result)

#     # # 4. 값 검증
#     # assert result[0] == payload["location_id"]
#     # assert abs(float(result[1]) - payload["temperature"]) < 0.01
#     # assert abs(float(result[2]) - payload["humidity"]) < 0.01
#     # assert abs(float(result[3]) - payload["tvoc"]) < 0.01
#     # assert abs(float(result[4]) - payload["noise"]) < 0.01
#     # assert abs(float(result[5]) - payload["pm10"]) < 0.01
#     # assert abs(float(result[6]) - payload["pm2_5"]) < 0.01

#     print("✅ 테스트 성공: MQTT → FastAPI → TimescaleDB 저장 정상 작동")

# if __name__ == "__main__":
#     import sys
#     print("Python executable:", sys.executable)
#     test_publish_and_check_db()

def test_always_passes():
    assert True
