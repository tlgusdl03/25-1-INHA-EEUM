# common_time.py
from datetime import datetime, timezone, timedelta

# UTC naive datetime을 테스트 전체에서 공유
def NOW():
    return datetime.now(timezone.utc).replace(tzinfo=None)

print("NOW():", NOW())
print("예상 기준 시각:", NOW() - timedelta(hours=3))
