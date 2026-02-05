from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select

from backend.entrance.database.db import SessionDep
from backend.entrance.database.models import Article, ArticleView, User
from backend.entrance.models.models import ViewCount, ViewOut
from backend.entrance.utils.auth import get_current_user

router = APIRouter(prefix="/views", tags=["views"])


def _view_to_out(view: ArticleView) -> ViewOut:
    return ViewOut(
        id=view.id,
        article_id=view.article_id,
        user_id=view.user_id,
        viewed_at=view.viewed_at,
    )


@router.post("/{article_id}", response_model=ViewOut, status_code=status.HTTP_201_CREATED)
async def register_view(
    article_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> ViewOut:
    article = await session.scalar(select(Article).where(Article.id == article_id))
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    view = ArticleView(
        article_id=article_id,
        user_id=user.id,
        viewed_at=datetime.now(timezone.utc),
    )
    session.add(view)
    await session.commit()
    await session.refresh(view)
    return _view_to_out(view)


@router.get("/{article_id}", response_model=ViewCount)
async def view_count(
    article_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> ViewCount:
    article = await session.scalar(select(Article).where(Article.id == article_id))
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    stmt = select(func.count(ArticleView.id)).where(ArticleView.article_id == article_id)
    count = await session.scalar(stmt)
    return ViewCount(article_id=article_id, count=count or 0)
