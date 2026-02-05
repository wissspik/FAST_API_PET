from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from backend.articles_service.routers import articles as articles_router
from backend.entrance.database.models import Article


def test_serialize_interests_trims_and_joins() -> None:
    result = articles_router._serialize_interests(["  python  ", "", "ai"])
    assert result == "python,ai"


def test_serialize_interests_empty_raises() -> None:
    with pytest.raises(HTTPException) as excinfo:
        articles_router._serialize_interests(["   ", ""])
    assert excinfo.value.status_code == 422


def test_article_to_out_parses_interests() -> None:
    article = Article(
        id=1,
        user_id=10,
        title="Title",
        content="Content",
        created_at=datetime(2026, 2, 1, tzinfo=timezone.utc),
        interests="one,two",
    )

    result = articles_router._article_to_out(article)

    assert result.id == 1
    assert result.interests == ["one", "two"]
