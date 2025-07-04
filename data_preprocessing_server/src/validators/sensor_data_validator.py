from models import SensorData

check_list = {
    "location_id": (int, (1, 10000)),  
    "temperature": (float, (-40, 85)),
    "humidity": (float, (0, 100)),
    "tvoc": (float, (0, 60000)),
    "noise": (float, (30, 130)),
    "pm10": (float, (0, 1000)),
    "pm2_5": (float, (0, 1000)),
}

# IoT 기기로부터 수신한 메시지에서 필수 필드 존재 확인, 타입 검사, 범위 검사 후 이상이 없으면 Sensor_Data ORM 객체 리턴
def data_validation_check(data: dict) -> SensorData:
    print("Validation_Check Start!")
    sensor_data = SensorData()

    for key, (expected_type, valid_range) in check_list.items():
        value = data.get(key)

        if value is None:
            print(f"{key} is missing")
            setattr(sensor_data, key, None)
            continue
        
        if expected_type == float and isinstance(value, int):
            value = float(value)

        elif not isinstance(value, expected_type):
            print(f"{key} must be of type {expected_type.__name__}")
            return None
        
        if not (valid_range[0] <= value <= valid_range[1]):
            print(f"{key} value {value} is out of range {valid_range}")
            return None
        
        else:
            setattr(sensor_data, key, value)

    return sensor_data

        
