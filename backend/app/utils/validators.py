"""
Validators module for data validation.
"""

import re
from typing import Tuple


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> bool:
    """
    Validate password strength.
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone.replace(' ', '').replace('-', '')) is not None


def validate_assessment_score(score: float, assessment_type: str) -> Tuple[bool, str]:
    """Validate assessment score is within acceptable range."""
    ranges = {
        'phq9': (0, 27),
        'gad7': (0, 21),
        'dass21': (0, 126),
        'pc_ptsd': (0, 4),
        'psqi': (0, 21)
    }
    
    if assessment_type not in ranges:
        return False, f"Unknown assessment type: {assessment_type}"
    
    min_score, max_score = ranges[assessment_type]
    if not min_score <= score <= max_score:
        return False, f"Score must be between {min_score} and {max_score}"
    
    return True, "Valid"


def validate_appointment_time(appointment_time) -> Tuple[bool, str]:
    """Validate appointment time is in future and during business hours."""
    from datetime import datetime
    
    now = datetime.utcnow()
    if appointment_time <= now:
        return False, "Appointment must be in the future"
    
    # Check if within business hours (8 AM to 6 PM)
    if appointment_time.hour < 8 or appointment_time.hour >= 18:
        return False, "Appointments available between 8 AM and 6 PM"
    
    return True, "Valid"


def validate_payment_amount(amount: float) -> Tuple[bool, str]:
    """Validate payment amount."""
    min_amount = 1000  # Minimum 1000 UGX
    max_amount = 10000000  # Maximum 10 million UGX
    
    if amount < min_amount:
        return False, f"Minimum amount is {min_amount}"
    if amount > max_amount:
        return False, f"Maximum amount is {max_amount}"
    
    return True, "Valid"
