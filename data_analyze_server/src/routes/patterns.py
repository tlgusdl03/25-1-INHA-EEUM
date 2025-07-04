from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from services.patterns import generate_pattern_report_service
from schemas.patterns import PatternResponse, ClusterRequest
from utils.cache import redis_client

router = APIRouter(prefix="/patterns", tags=["Patterns"])

@router.get("/", response_model=PatternResponse)
async def generate_pattern_report(
    params: ClusterRequest = Depends(),
    db: AsyncSession = Depends(get_db),
):
    key = f"pattern_cache:{params.location_id}:{params.lookback_days}"
    cached = await redis_client.get(key)

    if cached:
        return PatternResponse.model_validate_json(cached)
    
    result = await generate_pattern_report_service(
        db=db,
        request=params
    )
    await redis_client.set(key, result.model_dump_json(), ex=60 * 60 * 24)
    
    return result

@router.post("/invalidate-cache")
async def invalidate_all_pattern_cache():
    keys = []
    # SCAN 으로 pattern_cache:* 키 다 찾기
    async for key in redis_client.scan_iter(match="pattern_cache:*"):
        keys.append(key)

    if keys:
        await redis_client.delete(*keys)

    return {"success": True, "deleted_keys_count": len(keys)}
