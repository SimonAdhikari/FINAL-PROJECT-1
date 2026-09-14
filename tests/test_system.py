"""
Automated Test Suite for Secure User Management System.

Tests all functional requirements:
- Part A: Class Design, Encapsulation, Properties, Special Methods
- Part B: Inheritance, Super(), Method Overriding, Polymorphism
- Part C: Custom Exception Classes, Input Validation, Exception Handling
- Part D: Package Integrity
- Part E: Multithreaded Logging, Lockout Policy, Data Persistence & Export
"""

import os
import shutil
import time
import unittest
from secure_system import (
    User,
    Administrator,
    SecurityAnalyst,
    Validator,
    SecurityUtils,
    MultithreadedLogger,
    DataManager,
    InvalidEmailException,
    WeakPasswordException,
    InvalidUserIDException,
    AuthenticationFailedException,
    AccountLockedException,
)

TEST_DATA_DIR = "tests/test_data"


class TestSecureUserManagementSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_DATA_DIR, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DATA_DIR):
            shutil.rmtree(TEST_DATA_DIR, ignore_errors=True)

    def test_01_user_encapsulation_and_properties(self):
        """Test Part A: User encapsulation, properties, getters/setters, and password hashing."""
        admin = Administrator(
            user_id="ADM-001",
            name="Alice Smith",
            email="alice@cyberinst.edu",
            password="SecurePass123!",
            admin_level="SUPER_ADMIN"
        )
        self.assertEqual(admin.user_id, "ADM-001")
        self.assertEqual(admin.name, "Alice Smith")
        self.assertEqual(admin.email, "alice@cyberinst.edu")
        self.assertEqual(admin.role, "Administrator")
        
        # Verify direct access to private __password_hash is restricted
        with self.assertRaises(AttributeError):
            _ = admin.__password_hash  # Private attribute

        # Verify authentication
        self.assertTrue(admin.authenticate("SecurePass123!"))
        
        # Verify property setter
        admin.name = "Alice M. Smith"
        self.assertEqual(admin.name, "Alice M. Smith")

    def test_02_special_dunder_methods(self):
        """Test Part A: Overridden __str__, __repr__, and __eq__ methods."""
        u1 = SecurityAnalyst("ANA-101", "Bob Jones", "bob@cyberinst.edu", "AnalystP@ss1")
        u2 = SecurityAnalyst("ANA-101", "Bob Jones", "bob@cyberinst.edu", "AnalystP@ss1")
        u3 = SecurityAnalyst("ANA-102", "Charlie", "charlie@cyberinst.edu", "AnalystP@ss1")

        self.assertIn("ANA-101", str(u1))
        self.assertIn("SecurityAnalyst", repr(u1))
        self.assertEqual(u1, u2)
        self.assertNotEqual(u1, u3)

    def test_03_inheritance_and_polymorphism(self):
        """Test Part B: Inheritance, super(), and runtime polymorphism."""
        users: list[User] = [
            Administrator("ADM-002", "David Admin", "david@cyberinst.edu", "AdminP@ss123"),
            SecurityAnalyst("ANA-202", "Eve Analyst", "eve@cyberinst.edu", "AnalystP@ss123")
        ]

        # Polymorphic calls
        for user in users:
            privileges = user.get_privileges()
            task_output = user.execute_role_task()
            summary = user.generate_dashboard_summary()
            
            self.assertIsInstance(privileges, list)
            self.assertIsInstance(task_output, str)
            self.assertIsInstance(summary, dict)

        self.assertIn("FULL_SYSTEM_CONTROL", users[0].get_privileges())
        self.assertIn("VULNERABILITY_SCAN", users[1].get_privileges())

    def test_04_custom_exception_handling(self):
        """Test Part C: Custom exception triggering on invalid inputs."""
        # Invalid Email
        with self.assertRaises(InvalidEmailException):
            Validator.validate_email("invalid-email-format")

        # Weak Password (no special character)
        with self.assertRaises(WeakPasswordException):
            Validator.validate_password_strength("weakpassword123")

        # Invalid User ID format
        with self.assertRaises(InvalidUserIDException):
            Validator.validate_user_id("invalid_id_123")

    def test_05_account_lockout_policy(self):
        """Test Part E: Failed login tracking and account lockout."""
        analyst = SecurityAnalyst("ANA-303", "Frank Miller", "frank@cyberinst.edu", "FrankP@ss999!")
        
        # 2 failed attempts
        with self.assertRaises(AuthenticationFailedException):
            analyst.authenticate("WrongPass1")
        with self.assertRaises(AuthenticationFailedException):
            analyst.authenticate("WrongPass2")
        
        self.assertEqual(analyst.failed_login_attempts, 2)
        self.assertFalse(analyst.is_locked)

        # 3rd failed attempt triggers account lock
        with self.assertRaises(AccountLockedException):
            analyst.authenticate("WrongPass3")
        
        self.assertTrue(analyst.is_locked)

        # Subsequent attempts fail with AccountLockedException
        with self.assertRaises(AccountLockedException):
            analyst.authenticate("FrankP@ss999!")

        # Administrator unlocks user
        admin = Administrator("ADM-999", "Super Admin", "admin@cyberinst.edu", "SuperP@ss123!")
        admin.unlock_user(analyst)
        self.assertFalse(analyst.is_locked)
        self.assertEqual(analyst.failed_login_attempts, 0)
        self.assertTrue(analyst.authenticate("FrankP@ss999!"))

    def test_06_data_persistence_and_export(self):
        """Test Part E: JSON state persistence, CSV export, and activity report."""
        users = [
            Administrator("ADM-501", "Grace Hopper", "grace@cyberinst.edu", "GraceP@ss1!", "SUPER_ADMIN"),
            SecurityAnalyst("ANA-502", "Alan Turing", "alan@cyberinst.edu", "AlanP@ss1!", "TOP_SECRET", ["INC-101"])
        ]

        json_path = os.path.join(TEST_DATA_DIR, "users.json")
        csv_path = os.path.join(TEST_DATA_DIR, "export.csv")
        report_path = os.path.join(TEST_DATA_DIR, "report.txt")

        # Save and Load JSON
        DataManager.save_users_to_json(users, json_path)
        self.assertTrue(os.path.exists(json_path))

        loaded_users = DataManager.load_users_from_json(json_path)
        self.assertEqual(len(loaded_users), 2)
        self.assertEqual(loaded_users[0].user_id, "ADM-501")
        self.assertEqual(loaded_users[1].user_id, "ANA-502")
        self.assertTrue(loaded_users[0].authenticate("GraceP@ss1!"))

        # Export CSV
        DataManager.export_users_to_csv(users, csv_path)
        self.assertTrue(os.path.exists(csv_path))

        # Generate Activity Report
        report = DataManager.generate_activity_report(
            ["[2026-09-13] [User: ADM-501] [Action: LOGIN] [Status: SUCCESS]"],
            report_path
        )
        self.assertIn("CYBER SECURITY INSTITUTE", report)
        self.assertTrue(os.path.exists(report_path))

    def test_07_multithreaded_logger(self):
        """Test Part E: Asynchronous multithreaded logging."""
        log_file = os.path.join(TEST_DATA_DIR, "async_log.txt")
        logger = MultithreadedLogger(log_file)

        logger.log("ADM-001", "SYSTEM_CHECK", "SUCCESS", "Routine audit initiated.")
        logger.log("ANA-101", "VULN_SCAN", "SUCCESS", "Subnet scan completed.")
        
        # Give worker thread time to process queue
        time.sleep(0.5)
        logger.shutdown()

        self.assertTrue(os.path.exists(log_file))
        logs = logger.get_logs()
        self.assertGreaterEqual(len(logs), 2)


if __name__ == "__main__":
    unittest.main()
