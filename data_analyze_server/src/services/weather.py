from schemas.weather import FcstResponse, AirPollution
from core.config import KMA_SERVICE_KEY, KMA_VILAGE_FCST_URL, KMA_AIR_POLLUTION_INFORM
from datetime import datetime, timedelta
import httpx
from urllib.parse import unquote_plus

VALID_BASE_TIMES = ["0200","0500","0800","1100","1400","1700","2000","2300"]

def _latest_valid_basetime(now_kst):
    # 가장 가까운 앞선 base_time 선택
    hour_min = now_kst.strftime("%H%M")
    for bt in reversed(VALID_BASE_TIMES):
        if hour_min >= bt:
            return bt
    return "2300"  # 전날 23시

async def fetch_forecast(
    nx: int,
    ny: int,
    base_date: str | None = None,
    base_time: str | None = None,
    num_of_rows: int = 12,
    page_no: int = 1,
    data_type: str = "JSON",
) -> FcstResponse:
  # 기본값: 발표 기준 최근(현재-1시간) 시각
  now = datetime.now() - timedelta(hours=1)   # KST
  base_date = now.strftime("%Y%m%d")
  if(now.hour < 2):
     base_date = now - timedelta(days=1)
     base_date = base_date.strftime("%Y%m%d")
  base_time = _latest_valid_basetime(now)
  service_key = unquote_plus(KMA_SERVICE_KEY)
  params = {
      "serviceKey": service_key,
      "numOfRows": num_of_rows,
      "pageNo": page_no,
      "dataType": data_type,
      "base_date": base_date,
      "base_time": base_time,
      "nx": nx,
      "ny": ny,
  }
  async with httpx.AsyncClient(timeout=10.0) as client:
    r = await client.get(KMA_VILAGE_FCST_URL, params=params)
    r.raise_for_status()
    body = r.json()

    category_value_dict = {
      d["category"]: d["fcstValue"] for d in body["response"]["body"]["items"]["item"]
    }

    return FcstResponse(
      category_value_dict=category_value_dict
    )


async def fetch_air_pollution(
      returnType: str = "json",
      numOfRows: int = 1,
      pageNo: int = 1,
      searchDate: datetime = datetime.now(),
      informCode: str = "PM10"
) -> AirPollution:
    service_key = unquote_plus(KMA_SERVICE_KEY)
    params = {
      "serviceKey": service_key,
      "numOfRows": numOfRows,
      "pageNo": pageNo,
      "returnType": returnType,
      "searchDate": searchDate.strftime("%Y-%m-%d"),
      "informCode": informCode
    }
   
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(KMA_AIR_POLLUTION_INFORM, params=params)
        r.raise_for_status()
        body = r.json()
        
        try:
          informCause = body["response"]["body"]["items"][0]["informCause"]
          informOverall = body["response"]["body"]["items"][0]["informOverall"]

        except KeyError as e:
          raise RuntimeError(f"Unexpected API response format: {e}") from e

    return AirPollution(
      informCause=informCause,
      informOverall=informOverall
    )
