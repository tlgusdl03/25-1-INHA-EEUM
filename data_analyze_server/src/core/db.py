from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import DATABASE_URL

# 비동기 엔진 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=True,            # SQL 로그; 필요 없으면 False
    pool_pre_ping=True,   # 연결 유효성 확인
)

# 세션 팩토리
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()

# 의존성 주입용 헬퍼
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()