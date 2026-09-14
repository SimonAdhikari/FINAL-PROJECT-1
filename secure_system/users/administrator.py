"""
Administrator Class Module.

Implements Part B: Derived class Administrator inheriting from User.
Demonstrates method overriding, super() utilization, and runtime polymorphism.
"""

from secure_system.users.user import User

class Administrator(User):
    """
    Derived class representing an Administrator with elevated administrative privileges.
    Inherits core user capabilities from User base class.
    """

    DEFAULT_PRIVILEGES = [
        "USER_CREATE",
        "USER_READ",
        "USER_UPDATE",
        "USER_DELETE",
        "ACCOUNT_LOCK_UNLOCK",
        "SYSTEM_AUDIT_READ",
        "LOG_EXPORT",
    ]

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        password: str,
        admin_level: str = "SUPER_ADMIN",
        managed_departments: list[str] | None = None
    ):
        # Call superclass constructor (Part B requirement)
        super().__init__(user_id=user_id, name=name, email=email, password=password, role="Administrator")
        
        self.__admin_level = admin_level
        self.__managed_departments = managed_departments or ["IT Operations", "Cyber Security"]

    # --- PROPERTIES ---

    @property
    def admin_level(self) -> str:
        """Getter for Admin level."""
        return self.__admin_level

    @admin_level.setter
    def admin_level(self, level: str):
        """Setter for Admin level."""
        if not level or not isinstance(level, str):
            raise ValueError("Admin level must be a non-empty string.")
        self.__admin_level = level.upper()

    @property
    def managed_departments(self) -> list[str]:
        """Getter for managed departments."""
        return list(self.__managed_departments)

    def add_department(self, department: str):
        """Adds a department to managed list."""
        if department not in self.__managed_departments:
            self.__managed_departments.append(department)

    # --- POLYMORPHIC OVERRIDDEN METHODS (Part B) ---

    def get_privileges(self) -> list[str]:
        """Overrides base User method to return administrative permission set."""
        privileges = list(self.DEFAULT_PRIVILEGES)
        if self.__admin_level == "SUPER_ADMIN":
            privileges.append("FULL_SYSTEM_CONTROL")
        return privileges

    def execute_role_task(self) -> str:
        """Overrides base User method to perform administrator task."""
        return f"[ADMIN TASK] Administrator {self.name} (ID: {self.user_id}) performed System Audit and User Privilege Verification across departments: {', '.join(self.__managed_departments)}."

    def generate_dashboard_summary(self) -> dict:
        """Overrides base User summary to include admin-specific metrics."""
        summary = super().generate_dashboard_summary()
        summary.update({
            "Admin Level": self.__admin_level,
            "Managed Depts": ", ".join(self.__managed_departments),
            "Privilege Count": len(self.get_privileges())
        })
        return summary

    # --- ADMINISTRATIVE OPERATIONS ---

    def lock_user(self, target_user: User) -> str:
        """Locks a target user's account."""
        target_user.lock_account()
        return f"Administrator {self.name} locked account for User '{target_user.user_id}'."

    def unlock_user(self, target_user: User) -> str:
        """Unlocks a target user's account."""
        target_user.unlock_account()
        return f"Administrator {self.name} unlocked account for User '{target_user.user_id}'."

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} | Level: {self.__admin_level} | Depts: {len(self.__managed_departments)}"
