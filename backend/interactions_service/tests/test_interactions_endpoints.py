import asyncio
from datetime import datetime, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from backend.entrance.database.models import Article, Role, User
from backend.entrance.models.models import CommentCreate
from backend.interactions_service.routers.comments import create_comment
from backend.interactions_service.routers.likes import like_article


class FakeSession:
    def __init__(self, article: Article | None, commit_error: Exception | None = None) -> None:
        self.article = article
        self.commit_error = commit_error
        self.added = []
        self.rolled_back = False

    async def scalar(self, stmt):
        return self.article

    def add(self, obj) -> None:
        self.added.append(obj)

    async def commit(self) -> None:
        if self.commit_error:
            raise self.commit_error

    async def rollback(self) -> None:
        self.rolled_back = True

    async def refresh(self, obj) -> None:
        if getattr(obj, "id", None) is None:
            obj.id = 1


def _make_article() -> Article:
    return Article(
        id=1,
        user_id=10,
        title="Title",
        content="Content",
        created_at=datetime(2026, 2, 1, tzinfo=timezone.utc),
        interests="one,two",
    )


def _make_user() -> User:
    return User(id=7, login="user", password="x", role=Role.user)


def test_create_comment_success() -> None:
    article = _make_article()
    session = FakeSession(article)
    user = _make_user()
    data = CommentCreate(article_id=article.id, content="Nice post")

    result = asyncio.run(create_comment(data, session, user))

    assert result.article_id == article.id
    assert result.user_id == user.id
    assert result.content == "Nice post"
    assert result.id == 1


def test_like_article_conflict() -> None:
    article = _make_article()
    session = FakeSession(article, commit_error=IntegrityError("dup", None, None))
    user = _make_user()

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(like_article(article.id, session, user))

    assert excinfo.value.status_code == 409
    assert session.rolled_back is True
