from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple
from models.location import Location
from math import floor
from fastapi import HTTPException

#longtitude, langtitude
async def get_latlon_by_id(
    db: AsyncSession,
    location_id: int
) -> Tuple[int, int] | None:
    """
    location_id → (lat, lon)  튜플 반환. 없으면 None
    """
    row = (
        await db.execute(
            select(Location.coordinates).where(Location.location_id == location_id)
        )
    ).scalar_one_or_none()

    if row is None:            # id 없음
        return None

    lon_str, lat_str = row.split(",")
    return floor(float(lon_str[1:])+0.5), floor(float(lat_str[:-1])+0.5)

async def get_name(
    db: AsyncSession,
    location_id: int
):
    row = (
        await db.execute(
            select(Location.name)
            .where(Location.location_id == location_id)
        )
    ).scalar_one_or_none()

    if row is None:            # id 없음
      raise HTTPException(
            status_code=404,
            detail=f"No locationName for location_id={location_id}",
      )
      return None
    return row