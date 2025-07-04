from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DB_URL 환경변수가 설정되지 않았습니다.")

KMA_VILAGE_FCST_URL = (
    "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
)

KMA_AIR_POLLUTION_INFORM = (
    "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth"
)

KMA_SERVICE_KEY = os.getenv("KMA_SERVICE_KEY")
if not KMA_SERVICE_KEY:
    raise RuntimeError("KMA_SERVICE_KEY 환경변수가 없습니다.")
