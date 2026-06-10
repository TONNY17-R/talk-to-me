"""
Helper functions for common operations.
"""

from datetime import datetime, timedelta
import uuid
import string
import random


def generate_token(length: int = 32) -> str:
    """Generate a random token."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_verification_code(length: int = 6) -> str:
    """Generate numeric verification code."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def generate_uuid() -> str:
    """Generate UUID."""
    return str(uuid.uuid4())


def get_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.utcnow()


def format_date(date_obj: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """Format datetime object."""
    return date_obj.strftime(format_str) if date_obj else None


def days_between(start_date: datetime, end_date: datetime) -> int:
    """Calculate days between two dates."""
    return (end_date - start_date).days


def is_within_hours(start_time: datetime, hours: int) -> bool:
    """Check if time is within X hours from now."""
    return (datetime.utcnow() - start_time) < timedelta(hours=hours)


def truncate_text(text: str, length: int = 100, suffix: str = '...') -> str:
    """Truncate text to specified length."""
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = ''.join(c if c.isalnum() or c in ('-', '_') else '-' for c in text)
    text = '-'.join(filter(None, text.split('-')))
    return text


def paginate_query(query, page: int = 1, per_page: int = 20):
    """Paginate a SQLAlchemy query."""
    total = query.count()
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }


def dict_to_obj(data: dict):
    """Convert dictionary to object with dot notation access."""
    class DictObject:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
        
        def __repr__(self):
            return str(self.__dict__)
    
    return DictObject(**data)
