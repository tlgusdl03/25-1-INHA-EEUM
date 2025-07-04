from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import IoTDevice
from datetime import datetime
from utils.common_time import NOW

async def update_device_status(session: AsyncSession, location_id: int):
  result = await session.execute(
    select(IoTDevice).where(IoTDevice.location_id == location_id)
  )
  device = result.scalar_one_or_none()

  now = NOW()

  if device:
    print(f"🔄 기존 장치 상태 갱신: location_id={location_id}")
    device.status = "active"
    device.is_connected = True
    device.last_sent_at = now
  else:
    print(f"🆕 신규 장치 등록: location_id={location_id}")
    device = IoTDevice(
      location_id=location_id,
      status="active",
      is_connected=True,
      last_sent_at=now
    )
    session.add(device)
  
  await session.commit()
  print(f"✅ IoTDevice 상태 저장 완료: location_id={location_id}, time={now.isoformat()}")
