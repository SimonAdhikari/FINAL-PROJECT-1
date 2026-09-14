"""
Data Persistence and Storage Module.

Implements Part E requirement: File handling for storing user records,
JSON state persistence, CSV data export, and activity report generation.
"""

import os
import json
import csv
from secure_system.users import User, Administrator, SecurityAnalyst
from secure_system.exceptions import UserManagementException

class DataManager:
    """Handles JSON serialization, CSV export, and report generation."""

    @staticmethod
    def save_users_to_json(users: list[User], file_path: str = "data/users.json"):
        """
        Serializes a list of User objects into JSON format.
        Preserves polymorphic type information and encrypted credentials.
        """
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        serialized_data = []

        for user in users:
            record = {
                "class": user.__class__.__name__,
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "password_hash": user._get_password_hash(),
                "salt": user._get_salt(),
                "is_active": user.is_active,
                "is_locked": user.is_locked,
                "failed_login_attempts": user.failed_login_attempts,
                "created_at": user.created_at,
                "last_login": user.last_login
            }

            if isinstance(user, Administrator):
                record["admin_level"] = user.admin_level
                record["managed_departments"] = user.managed_departments
            elif isinstance(user, SecurityAnalyst):
                record["clearance_level"] = user.clearance_level
                record["assigned_incidents"] = user.assigned_incidents

            serialized_data.append(record)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(serialized_data, f, indent=4)

    @staticmethod
    def load_users_from_json(file_path: str = "data/users.json") -> list[User]:
        """
        Loads and reconstructs polymorphic User objects from JSON file.
        """
        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            users = []
            for item in data:
                cls_name = item.get("class", "User")
                
                # Note: We pass dummy password because _set_security_credentials will restore actual hash/salt
                dummy_pass = "P@ssword123!"

                if cls_name == "Administrator":
                    user = Administrator(
                        user_id=item["user_id"],
                        name=item["name"],
                        email=item["email"],
                        password=dummy_pass,
                        admin_level=item.get("admin_level", "SUPER_ADMIN"),
                        managed_departments=item.get("managed_departments", [])
                    )
                elif cls_name == "SecurityAnalyst":
                    user = SecurityAnalyst(
                        user_id=item["user_id"],
                        name=item["name"],
                        email=item["email"],
                        password=dummy_pass,
                        clearance_level=item.get("clearance_level", "SECRET"),
                        assigned_incidents=item.get("assigned_incidents", [])
                    )
                else:
                    raise UserManagementException(f"Unknown user class '{cls_name}'.")

                # Restore exact cryptographic security state & flags
                user._set_security_credentials(
                    password_hash=item["password_hash"],
                    salt=item["salt"],
                    is_active=item["is_active"],
                    is_locked=item["is_locked"],
                    failed_attempts=item["failed_login_attempts"],
                    last_login=item.get("last_login")
                )
                users.append(user)

            return users
        except Exception as e:
            raise UserManagementException(f"Failed to load user repository from JSON: {e}")

    @staticmethod
    def export_users_to_csv(users: list[User], csv_path: str = "data/user_directory_export.csv"):
        """
        Exports user directory details into CSV format.
        Excludes raw salt and sensitive credentials for security.
        """
        os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
        headers = ["User ID", "Name", "Email", "Role", "Class", "Active", "Locked", "Failed Attempts", "Last Login"]

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for user in users:
                writer.writerow([
                    user.user_id,
                    user.name,
                    user.email,
                    user.role,
                    user.__class__.__name__,
                    "Yes" if user.is_active else "No",
                    "Yes" if user.is_locked else "No",
                    user.failed_login_attempts,
                    user.last_login or "N/A"
                ])

    @staticmethod
    def generate_activity_report(log_entries: list[str], report_path: str = "data/activity_report.txt") -> str:
        """
        Generates a structured system activity summary report.
        """
        os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)
        
        total_logs = len(log_entries)
        success_count = sum(1 for line in log_entries if "[Status: SUCCESS]" in line)
        failure_count = sum(1 for line in log_entries if "[Status: FAILURE]" in line or "LOCKED" in line)

        report_content = [
            "=" * 70,
            "               CYBER SECURITY INSTITUTE - SYSTEM AUDIT REPORT",
            "=" * 70,
            f"Report Generated At: {os.sys.platform} - Audit Timestamp",
            f"Total Activities Logged: {total_logs}",
            f"Successful Operations: {success_count}",
            f"Failed / Security Events: {failure_count}",
            "-" * 70,
            "RECENT ACTIVITY LOG ENTRIES:",
            "-" * 70
        ]

        report_content.extend(log_entries[-30:] if log_entries else ["No activity logs recorded."])
        report_content.append("=" * 70)

        formatted_report = "\n".join(report_content)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(formatted_report)

        return formatted_report
