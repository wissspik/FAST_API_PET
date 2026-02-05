from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from backend.entrance.database.db import SessionDep
from backend.entrance.database.models import Article, Like, User
from backend.entrance.models.models import LikeCount, LikeOut
from backend.entrance.utils.auth import get_current_user

router = APIRouter(prefix="/likes", tags=["likes"])


def _like_to_out(like: Like) -> LikeOut:
    return LikeOut(
        id=like.id,
        article_id=like.article_id,
        user_id=like.user_id,
        created_at=like.created_at,
    )


@router.post("/{article_id}", response_model=LikeOut, status_code=status.HTTP_201_CREATED)
async def like_article(
    article_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> LikeOut:
    article = await session.scalar(select(Article).where(Article.id == article_id))
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    like = Like(
        article_id=article_id,
        user_id=user.id,
        created_at=datetime.now(timezone.utc),
    )
    session.add(like)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Article already liked")
    await session.refresh(like)
    return _like_to_out(like)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_article(
    article_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> None:
    stmt = select(Like).where(Like.article_id == article_id, Like.user_id == user.id)
    like = await session.scalar(stmt)
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    await session.delete(like)
    await session.commit()
    return None


@router.get("/{article_id}", response_model=LikeCount)
async def like_count(
    article_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> LikeCount:
    article = await session.scalar(select(Article).where(Article.id == article_id))
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    stmt = select(func.count(Like.id)).where(Like.article_id == article_id)
    count = await session.scalar(stmt)
    return LikeCount(article_id=article_id, count=count or 0)
