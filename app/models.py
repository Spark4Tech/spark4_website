# app/models.py

from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

class Contact(db.Model):
    """Model for storing early access registration submissions."""
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )
    responded: Mapped[bool] = mapped_column(default=False)
    response_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship("BlogPost", back_populates="author")

class Category(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="category")

    def generate_slug(self):
        from slugify import slugify
        self.slug = slugify(self.name)

class Tag(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(secondary="post_tags", back_populates="tags")

post_tags = Table(
    "post_tags",
    db.metadata,
    db.Column("post_id", ForeignKey("blog_post.id"), primary_key=True),
    db.Column("tag_id", ForeignKey("tag.id"), primary_key=True)
)

class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))
    category: Mapped[Optional[Category]] = relationship(back_populates="posts")
    tags: Mapped[List[Tag]] = relationship(secondary=post_tags, back_populates="posts")
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)
    author: Mapped["Author"] = relationship("Author", back_populates="posts")
    featured_image: Mapped[Optional[str]] = mapped_column(String(200))
    featured_image_alt: Mapped[Optional[str]] = mapped_column(String(300))
    inside_image: Mapped[Optional[str]] = mapped_column(String(200))
    inside_image_alt: Mapped[Optional[str]] = mapped_column(String(300))
    featured_image_caption: Mapped[Optional[str]] = mapped_column(String(200))
    inside_image_caption: Mapped[Optional[str]] = mapped_column(String(200))


    def generate_slug(self) -> None:
        from slugify import slugify
        self.slug = slugify(self.title)

class BlogPostData:
    def __init__(self):
        self.title = ""
        self.date = ""
        self.author = ""
        self.category = ""
        self.tags = []
        self.featured_image = ""
        self.featured_image_alt = ""
        self.inside_image = ""
        self.inside_image_alt = ""
        self.featured_image_caption = ""
        self.inside_image_caption = ""
        self.excerpt = ""
        self.content = ""
        self.published = True

    @classmethod
    def from_dict(cls, data):
        post = cls()
        post.__dict__.update(data)
        return post