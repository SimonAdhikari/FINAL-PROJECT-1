"""
Secure User Management System Package.

A modular Object-Oriented User Management System for Cyber Security Institutes.
Exposes core classes, exceptions, storage, and utilities.
"""

from secure_system.users import User, Administrator, SecurityAnalyst
from secure_system.exceptions import (
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
from secure_system.utilities import Validator, SecurityUtils, MultithreadedLogger
from secure_system.storage import DataManager

__version__ = "1.0.0"
__author__ = "Cyber Security Institute Dev Team"

__all__ = [
    "User",
    "Administrator",
    "SecurityAnalyst",
    "UserManagementException",
    "InvalidEmailException",
    "WeakPasswordException",
    "InvalidUserIDException",
    "AuthenticationFailedException",
    "AccountLockedException",
    "PermissionDeniedException",
    "UserAlreadyExistsException",
    "UserNotFoundException",
    "Validator",
    "SecurityUtils",
    "MultithreadedLogger",
    "DataManager",
]
