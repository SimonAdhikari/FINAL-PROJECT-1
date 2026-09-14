"""
Exceptions Package Initialization.
"""

from .custom_exceptions import (
    UserManagementException,
    InvalidEmailException,
    WeakPasswordException,
    InvalidUserIDException,
    AuthenticationFailedException,
    AccountLockedException,
    PermissionDeniedException,
    UserAlreadyExistsException,
    UserNotFoundException,
)

__all__ = [
    "UserManagementException",
    "InvalidEmailException",
    "WeakPasswordException",
    "InvalidUserIDException",
    "AuthenticationFailedException",
    "AccountLockedException",
    "PermissionDeniedException",
    "UserAlreadyExistsException",
    "UserNotFoundException",
]
