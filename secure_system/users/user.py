"""
Base User Class Module.

Implements Part A: Class Design and Encapsulation.
Serves as the abstract/base class for all user roles in the Secure User Management System.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from secure_system.utilities import Validator, SecurityUtils
from secure_system.exceptions import (
    AuthenticationFailedException,
    AccountLockedException,
    WeakPasswordException,
)

class User(ABC):
    """
    Base class representing a system user with encapsulated attributes,
    salted password hashing, and account security controls.
    """

    MAX_FAILED_ATTEMPTS = 3

    def __init__(self, user_id: str, name: str, email: str, password: str, role: str = "Standard User"):
        # Validate inputs via Validator utility
        self.__user_id = Validator.validate_user_id(user_id)
        self.__name = Validator.validate_name(name)
        self.__email = Validator.validate_email(email)
        self.__role = role
        
        # Encapsulated security credentials
        Validator.validate_password_strength(password)
        self.__salt = SecurityUtils.generate_salt()
        self.__password_hash = SecurityUtils.hash_password(password, self.__salt)
        
        # Account status flags
        self.__is_active = True
        self.__failed_login_attempts = 0
        self.__is_locked = False
        self.__created_at = datetime.now().isoformat()
        self.__last_login = None

    # --- ENCAPSULATION & PROPERTIES ---

    @property
    def user_id(self) -> str:
        """Getter for User ID."""
        return self.__user_id

    @property
    def name(self) -> str:
        """Getter for User Name."""
        return self.__name

    @name.setter
    def name(self, new_name: str):
        """Setter for User Name with validation."""
        self.__name = Validator.validate_name(new_name)

    @property
    def email(self) -> str:
        """Getter for Email."""
        return self.__email

    @email.setter
    def email(self, new_email: str):
        """Setter for Email with validation."""
        self.__email = Validator.validate_email(new_email)

    @property
    def role(self) -> str:
        """Getter for Role."""
        return self.__role

    @property
    def is_active(self) -> bool:
        """Getter for Account Active Status."""
        return self.__is_active

    @property
    def is_locked(self) -> bool:
        """Getter for Account Lockout Status."""
        return self.__is_locked

    @property
    def failed_login_attempts(self) -> int:
        """Getter for consecutive failed login attempts."""
        return self.__failed_login_attempts

    @property
    def created_at(self) -> str:
        """Getter for creation timestamp."""
        return self.__created_at

    @property
    def last_login(self) -> str | None:
        """Getter for last login timestamp."""
        return self.__last_login

    # Internal accessors for serialization
    def _get_password_hash(self) -> str:
        return self.__password_hash

    def _get_salt(self) -> str:
        return self.__salt

    def _set_security_credentials(self, password_hash: str, salt: str, is_active: bool, is_locked: bool, failed_attempts: int, last_login: str | None = None):
        """Internal helper used during JSON deserialization to restore account state."""
        self.__password_hash = password_hash
        self.__salt = salt
        self.__is_active = is_active
        self.__is_locked = is_locked
        self.__failed_login_attempts = failed_attempts
        self.__last_login = last_login

    # --- SECURITY & AUTHENTICATION METHODS ---

    def authenticate(self, password: str) -> bool:
        """
        Authenticates the user against stored password hash.
        Handles Part E: Login Attempt Tracker & Account Lockout Policy.
        """
        if self.__is_locked:
            raise AccountLockedException(self.__user_id)

        if not self.__is_active:
            raise AuthenticationFailedException(f"Account '{self.__user_id}' is deactivated.")

        is_valid = SecurityUtils.verify_password(password, self.__password_hash, self.__salt)

        if is_valid:
            self.__failed_login_attempts = 0
            self.__last_login = datetime.now().isoformat()
            return True
        else:
            self.__failed_login_attempts += 1
            if self.__failed_login_attempts >= self.MAX_FAILED_ATTEMPTS:
                self.lock_account()
                raise AccountLockedException(self.__user_id)
            raise AuthenticationFailedException(
                f"Invalid credentials. Attempt {self.__failed_login_attempts}/{self.MAX_FAILED_ATTEMPTS} before lockout."
            )

    def change_password(self, old_password: str, new_password: str) -> bool:
        """Verifies old password, validates strength of new password, and updates hash."""
        if not SecurityUtils.verify_password(old_password, self.__password_hash, self.__salt):
            raise AuthenticationFailedException("Current password verification failed.")

        Validator.validate_password_strength(new_password)
        self.__salt = SecurityUtils.generate_salt()
        self.__password_hash = SecurityUtils.hash_password(new_password, self.__salt)
        return True

    def lock_account(self):
        """Locks user account due to security policy."""
        self.__is_locked = True

    def unlock_account(self):
        """Unlocks user account and resets failure counters."""
        self.__is_locked = False
        self.__failed_login_attempts = 0

    def deactivate_account(self):
        """Deactivates account."""
        self.__is_active = False

    def activate_account(self):
        """Activates account."""
        self.__is_active = True

    # --- POLYMORPHIC INTERFACE METHODS (Part B) ---

    @abstractmethod
    def get_privileges(self) -> list[str]:
        """Returns a list of role-based permission privileges."""
        pass

    @abstractmethod
    def execute_role_task(self) -> str:
        """Executes a primary operational task defined by user's role."""
        pass

    def generate_dashboard_summary(self) -> dict:
        """Generates a summary dictionary of user status for dashboard display."""
        return {
            "User ID": self.__user_id,
            "Name": self.__name,
            "Email": self.__email,
            "Role": self.__role,
            "Active": "Yes" if self.__is_active else "No",
            "Locked": "LOCKED" if self.__is_locked else "Normal",
            "Last Login": self.__last_login or "Never"
        }

    # --- SPECIAL DUNDER METHODS OVERRIDES (Part A) ---

    def __str__(self) -> str:
        status = "LOCKED" if self.__is_locked else ("ACTIVE" if self.__is_active else "INACTIVE")
        return f"User[{self.__user_id}] | Name: {self.__name} | Email: {self.__email} | Role: {self.__role} | Status: {status}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(user_id='{self.__user_id}', role='{self.__role}')>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.__user_id == other.user_id
