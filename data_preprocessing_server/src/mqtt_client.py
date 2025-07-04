import json
import asyncio
from datetime import datetime
import paho.mqtt.client as mqtt

from database import async_session
from models import SensorData  
from preprocessors.missing_handler import missing_data_check
from preprocessors.outlier_handler import outlier_data_check
from device_manager.update_device_status import update_device_status
from utils.common_time import NOW

loop = None

def init(loop_from_main):
    global loop
    loop = loop_from_main

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("받은 메시지:", payload)

        coro = save_sensor_data(payload)
        asyncio.run_coroutine_threadsafe(coro, loop)

    except Exception as e:
        import traceback
        print("❌ MQTT 메시지 처리 오류:")
        traceback.print_exc()

async def save_sensor_data(data):
    try:
        # SensorData 객체로 변환
        sensor_data = SensorData(
            location_id=data["location_id"],
            collected_at=NOW(),
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            tvoc=data.get("tvoc"),
            noise=data.get("noise"),
            pm10=data.get("pm10"),
            pm2_5=data.get("pm2_5")
        )

        # # 1️⃣ 이상치 처리
        # sensor_data = await outlier_data_check(sensor_data)

        # 2️⃣ 결측치 처리
        sensor_data = await missing_data_check(sensor_data)

        async with async_session() as session:
            await update_device_status(session, sensor_data.location_id)
            session.add(sensor_data)
            await session.commit()
            print("✅전처리 후 DB 저장 완료")
            
    except Exception as e:
        import traceback
        print("❌ DB 저장 중 예외 발생:")
        traceback.print_exc()

def run_mqtt():
    print("✅ MQTT 클라이언트 시작 중...")

    client = mqtt.Client()
    client.on_message = on_message
    client.connect("mosquitto", 1883)  # 도커 컨테이너 이름 기준
    client.subscribe("sensors/data")
    print("✅ MQTT 연결 및 구독 완료")
    client.loop_forever()
