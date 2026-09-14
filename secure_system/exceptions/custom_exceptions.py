"""
Custom Exception Classes for Secure User Management System.

Demonstrates Part C requirement: Exception Handling with custom exception hierarchy.
"""

class UserManagementException(Exception):
    """Base exception class for all Secure User Management System errors."""
    def __init__(self, message: str, code: str = "ERR_GENERAL"):
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class InvalidEmailException(UserManagementException):
    """Raised when an email address fails validation rules."""
    def __init__(self, email: str, details: str = "Email format is invalid."):
        super().__init__(f"Invalid Email '{email}': {details}", code="ERR_INVALID_EMAIL")
        self.email = email


class WeakPasswordException(UserManagementException):
    """Raised when a password does not meet security strength requirements."""
    def __init__(self, reasons: list[str] | None = None):
        reason_str = "; ".join(reasons) if reasons else "Password does not meet complexity requirements."
        super().__init__(f"Weak Password: {reason_str}", code="ERR_WEAK_PASSWORD")
        self.reasons = reasons or []


class InvalidUserIDException(UserManagementException):
    """Raised when a User ID violates formatting conventions."""
    def __init__(self, user_id: str, details: str = "User ID format is invalid."):
        super().__init__(f"Invalid User ID '{user_id}': {details}", code="ERR_INVALID_USER_ID")
        self.user_id = user_id


class AuthenticationFailedException(UserManagementException):
    """Raised when authentication fails due to incorrect password or locked account."""
    def __init__(self, details: str = "Authentication failed due to invalid credentials."):
        super().__init__(details, code="ERR_AUTH_FAILED")


class AccountLockedException(AuthenticationFailedException):
    """Raised when attempting login on a locked account."""
    def __init__(self, user_id: str):
        super().__init__(f"Account for User ID '{user_id}' is locked due to security policy.")


class PermissionDeniedException(UserManagementException):
    """Raised when a user lacks required role permissions for an operation."""
    def __init__(self, role: str, operation: str):
        super().__init__(f"Permission Denied: Role '{role}' cannot perform '{operation}'.", code="ERR_PERMISSION_DENIED")
        self.role = role
        self.operation = operation


class UserAlreadyExistsException(UserManagementException):
    """Raised when registering a user ID or email that already exists."""
    def __init__(self, identifier: str):
        super().__init__(f"User with identifier '{identifier}' already exists in system.", code="ERR_USER_EXISTS")


class UserNotFoundException(UserManagementException):
    """Raised when a requested user cannot be found in persistence or repository."""
    def __init__(self, user_id: str):
        super().__init__(f"User with ID '{user_id}' was not found.", code="ERR_USER_NOT_FOUND")
