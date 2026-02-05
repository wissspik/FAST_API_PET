from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from backend.entrance.database.db import SessionDep
from backend.entrance.database.models import Article, Comment, User
from backend.entrance.models.models import CommentCreate, CommentOut
from backend.entrance.utils.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])


def _comment_to_out(comment: Comment) -> CommentOut:
    return CommentOut(
        id=comment.id,
        article_id=comment.article_id,
        user_id=comment.user_id,
        content=comment.content,
        created_at=comment.created_at,
    )


@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(
    data: CommentCreate,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> CommentOut:
    article = await session.scalar(select(Article).where(Article.id == data.article_id))
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    comment = Comment(
        article_id=data.article_id,
        user_id=user.id,
        content=data.content,
        created_at=datetime.now(timezone.utc),
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return _comment_to_out(comment)


@router.get("/article/{article_id}", response_model=list[CommentOut])
async def list_comments(
    article_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> list[CommentOut]:
    article = await session.scalar(select(Article).where(Article.id == article_id))
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    stmt = select(Comment).where(Comment.article_id == article_id).order_by(Comment.created_at.asc())
    result = await session.scalars(stmt)
    return [_comment_to_out(comment) for comment in result.all()]


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> None:
    stmt = select(Comment).where(Comment.id == comment_id, Comment.user_id == user.id)
    comment = await session.scalar(stmt)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    await session.delete(comment)
    await session.commit()
    return None
