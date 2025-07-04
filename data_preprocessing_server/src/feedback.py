# from pydanticModels import FeedbackCreate
# from utils import NOW
# from models import Feedback
# from database import get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends

# async def feedback_create(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
#     db_feedback = Feedback(
#         location_id=feedback.location_id,
#         satisfaction_score=feedback.satisfaction_score,
#         created_at=NOW(),
#         used_for_training=False
#     )
#     db.add(db_feedback)
#     await db.commit()
#     await db.refresh(db_feedback)
#     return db_feedback


# def feedback_get_by_location_id(location_id: int):
#     pass
