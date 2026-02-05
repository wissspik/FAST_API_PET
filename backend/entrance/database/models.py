from sqlalchemy import Integer, String,DateTime,ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
import enum
from sqlalchemy import Enum

class Role(enum.Enum):
    admin = "admin"
    user = "user"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, index=True, unique=True
    )
    login: Mapped[str] = mapped_column(
        String(30), index=True, nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(
        String(136), nullable=False, unique=False, index=True
    )
    role: Mapped[Role] = mapped_column(
        Enum(Role), nullable=False, unique=False, index=False
    )
    email: Mapped[str] = mapped_column(
        String(120), nullable=True, unique=True, index=True
    )
    phone: Mapped[str] = mapped_column(
        String(11), unique=True, nullable=True, index=True
    )
    articles: Mapped[list["Article"]] = relationship(
        back_populates="user",
        cascade="all"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="user",
        cascade="all"
    )
    likes: Mapped[list["Like"]] = relationship(
        back_populates="user",
        cascade="all"
    )
    views: Mapped[list["ArticleView"]] = relationship(
        back_populates="user",
        cascade="all"
    )
class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, index=True, unique=True
    )
    # Внешний ключ указывает на User
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(256), index=True, nullable=False, unique=False
    )
    content: Mapped[str] = mapped_column(
        String(1500), nullable=False, unique=False
    )
    created_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    interests : Mapped[str] = mapped_column(
        String(256), index=True, nullable=False, unique=True
    )
    # обратная связь
    user: Mapped["User"] = relationship(
        back_populates="articles"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="article",
        cascade="all"
    )
    likes: Mapped[list["Like"]] = relationship(
        back_populates="article",
        cascade="all"
    )
    views: Mapped[list["ArticleView"]] = relationship(
        back_populates="article",
        cascade="all"
    )


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, index=True, unique=True
    )
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    content: Mapped[str] = mapped_column(
        String(1000), nullable=False, unique=False
    )
    created_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="comments"
    )
    article: Mapped["Article"] = relationship(
        back_populates="comments"
    )


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("article_id", "user_id", name="uq_likes_article_user"),
    )
    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, index=True, unique=True
    )
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    created_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="likes"
    )
    article: Mapped["Article"] = relationship(
        back_populates="likes"
    )


class ArticleView(Base):
    __tablename__ = "article_views"
    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, index=True, unique=True
    )
    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    viewed_at : Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="views"
    )
    article: Mapped["Article"] = relationship(
        back_populates="views"
    )
