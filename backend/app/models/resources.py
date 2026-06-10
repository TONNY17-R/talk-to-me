"""
Resources models for Talk to Me platform.

This module contains models for managing mental health resources and content.
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class ResourceType(str, Enum):
    """Enum for different types of resources."""
    ARTICLE = "article"
    VIDEO = "video"
    PODCAST = "podcast"
    BOOK = "book"
    GUIDE = "guide"
    EXERCISE = "exercise"
    MEDITATION = "meditation"
    TOOL = "tool"
    SUPPORT_GROUP = "support_group"
    HOTLINE = "hotline"


class ResourceCategory(str, Enum):
    """Enum for resource categories."""
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    STRESS = "stress"
    SLEEP = "sleep"
    RELATIONSHIPS = "relationships"
    SELF_ESTEEM = "self_esteem"
    SUBSTANCE_ABUSE = "substance_abuse"
    TRAUMA = "trauma"
    CRISIS = "crisis"
    GENERAL_WELLNESS = "general_wellness"


class Resource:
    """
    Represents a mental health resource (article, video, guide, etc.).
    
    Attributes:
        id: Unique identifier for the resource
        title: Title of the resource
        description: Description/summary of the resource
        resource_type: Type of resource (article, video, etc.)
        category: Category of the resource
        content: Full content of the resource
        author: Author/creator of the resource
        source_url: URL to external resource if applicable
        is_external: Whether this links to external content
        is_published: Whether the resource is published
        is_featured: Whether this is a featured resource
        views_count: Number of times the resource has been viewed
        created_at: When the resource was created
        updated_at: When the resource was last updated
    """
    __tablename__ = 'resources'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    resource_type = Column(SQLEnum(ResourceType), nullable=False)
    category = Column(SQLEnum(ResourceCategory), nullable=False)
    content = Column(Text, nullable=True)
    author = Column(String(255), nullable=True)
    source_url = Column(String(500), nullable=True)
    is_external = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # Relationships
    creator = relationship('User', backref='created_resources')
    bookmarks = relationship('UserBookmark', back_populates='resource', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f"<Resource id={self.id} title={self.title} type={self.resource_type}>"
    
    def to_dict(self) -> dict:
        """Convert resource to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'resource_type': self.resource_type.value if self.resource_type else None,
            'category': self.category.value if self.category else None,
            'author': self.author,
            'source_url': self.source_url,
            'is_external': self.is_external,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
            'views_count': self.views_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ResourceCategory:
    """
    Represents a category/collection of resources.
    
    Attributes:
        id: Unique identifier for the category
        name: Name of the category
        description: Description of the category
        icon: Icon identifier/URL for the category
        order: Display order of the category
        is_active: Whether this category is active
    """
    __tablename__ = 'resource_categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<ResourceCategory id={self.id} name={self.name}>"
    
    def to_dict(self) -> dict:
        """Convert category to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'order': self.order,
            'is_active': self.is_active
        }


class UserBookmark:
    """
    Represents a user's bookmark of a resource.
    
    Attributes:
        id: Unique identifier for the bookmark
        user_id: Foreign key to the User
        resource_id: Foreign key to the Resource
        notes: User's personal notes about the resource
        bookmarked_at: When the resource was bookmarked
        folder: Optional folder/collection name for organizing bookmarks
    """
    __tablename__ = 'user_bookmarks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    notes = Column(Text, nullable=True)
    folder = Column(String(100), nullable=True)
    bookmarked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', backref='bookmarks')
    resource = relationship('Resource', back_populates='bookmarks')
    
    def __repr__(self) -> str:
        return f"<UserBookmark id={self.id} user_id={self.user_id} resource_id={self.resource_id}>"
    
    def to_dict(self) -> dict:
        """Convert bookmark to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resource_id': self.resource_id,
            'notes': self.notes,
            'folder': self.folder,
            'bookmarked_at': self.bookmarked_at.isoformat() if self.bookmarked_at else None,
            'resource': self.resource.to_dict() if self.resource else None
        }
