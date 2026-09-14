"""
Validator Utility Module.

Implements input validation routines for User IDs, Emails, Passwords, and Names.
Raises custom exceptions when validation fails.
"""

import re
from secure_system.exceptions import (
    InvalidEmailException,
    WeakPasswordException,
    InvalidUserIDException,
)

class Validator:
    """Provides static validation methods for system inputs."""

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    USER_ID_REGEX = re.compile(r"^[A-Z]{3}-\d{3,6}$")  # e.g., USR-001, ADM-101, ANA-505

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validates an email address.
        Raises InvalidEmailException if validation fails.
        """
        if not email or not isinstance(email, str):
            raise InvalidEmailException(str(email), "Email cannot be empty.")
        
        cleaned_email = email.strip()
        if not Validator.EMAIL_REGEX.match(cleaned_email):
            raise InvalidEmailException(cleaned_email, "Does not conform to standard format (user@domain.com).")
        
        return cleaned_email

    @staticmethod
    def validate_user_id(user_id: str) -> str:
        """
        Validates User ID format.
        Must follow pattern: 3 uppercase letters, hyphen, 3-6 digits (e.g. USR-001, ADM-100).
        Raises InvalidUserIDException if format is invalid.
        """
        if not user_id or not isinstance(user_id, str):
            raise InvalidUserIDException(str(user_id), "User ID cannot be empty.")
        
        cleaned_id = user_id.strip().upper()
        if not Validator.USER_ID_REGEX.match(cleaned_id):
            raise InvalidUserIDException(
                cleaned_id, 
                "User ID must be formatted as 3 uppercase letters, hyphen, and 3-6 digits (e.g., ADM-001, ANA-002, USR-101)."
            )
        
        return cleaned_id

    @staticmethod
    def validate_password_strength(password: str) -> str:
        """
        Validates password strength against cyber security standards:
        - At least 8 characters long
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 digit
        - At least 1 special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
        
        Raises WeakPasswordException if any condition fails.
        """
        if not password or not isinstance(password, str):
            raise WeakPasswordException(["Password cannot be empty."])

        reasons = []
        if len(password) < 8:
            reasons.append("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            reasons.append("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            reasons.append("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            reasons.append("Password must contain at least one numerical digit.")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password):
            reasons.append("Password must contain at least one special character.")

        if reasons:
            raise WeakPasswordException(reasons)

        return password

    @staticmethod
    def validate_name(name: str) -> str:
        """Validates that a name string is non-empty and contains valid characters."""
        if not name or not isinstance(name, str) or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        return name.strip()
