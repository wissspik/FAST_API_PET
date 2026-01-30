from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.entrance.database.db import SessionDep
from backend.entrance.database.models import Article, User
from backend.entrance.models.models import ArticleCreate, ArticleOut, ArticleUpdate
from backend.entrance.utils.auth import get_current_user

router = APIRouter(prefix="/articles", tags=["articles"])


def _serialize_interests(interests: list[str]) -> str:
    cleaned = [item.strip() for item in interests if item and item.strip()]
    if not cleaned:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Interests must not be empty",
        )
    value = ",".join(cleaned)
    if len(value) > 256:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Interests too long",
        )
    return value


def _parse_interests(value: str) -> list[str]:
    return [item for item in value.split(",") if item]


def _article_to_out(article: Article) -> ArticleOut:
    return ArticleOut(
        id=article.id,
        title=article.title,
        content=article.content,
        interests=_parse_interests(article.interests),
        created_at=article.created_at,
    )


@router.post("", response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
async def create_article(
    data: ArticleCreate,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> ArticleOut:
    article = Article(
        user_id=user.id,
        title=data.title,
        content=data.content,
        created_at=datetime.now(timezone.utc),
        interests=_serialize_interests(data.interests),
    )
    session.add(article)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Article with same interests already exists",
        )
    await session.refresh(article)
    return _article_to_out(article)


@router.get("", response_model=list[ArticleOut])
async def list_articles(
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> list[ArticleOut]:
    stmt = select(Article).where(Article.user_id == user.id).order_by(Article.created_at.desc())
    result = await session.scalars(stmt)
    return [_article_to_out(article) for article in result.all()]


@router.get("/{article_id}", response_model=ArticleOut)
async def get_article(
    article_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> ArticleOut:
    stmt = select(Article).where(Article.id == article_id, Article.user_id == user.id)
    article = await session.scalar(stmt)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return _article_to_out(article)


@router.patch("/{article_id}", response_model=ArticleOut)
async def update_article(
    article_id: int,
    data: ArticleUpdate,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> ArticleOut:
    stmt = select(Article).where(Article.id == article_id, Article.user_id == user.id)
    article = await session.scalar(stmt)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    if data.title is None and data.content is None and data.interests is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    if data.title is not None:
        article.title = data.title
    if data.content is not None:
        article.content = data.content
    if data.interests is not None:
        article.interests = _serialize_interests(data.interests)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Article with same interests already exists",
        )
    await session.refresh(article)
    return _article_to_out(article)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
) -> None:
    stmt = select(Article).where(Article.id == article_id, Article.user_id == user.id)
    article = await session.scalar(stmt)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    await session.delete(article)
    await session.commit()
    return None
