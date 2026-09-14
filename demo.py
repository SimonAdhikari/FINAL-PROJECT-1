"""
Automated End-to-End System Demonstration Script.

Showcases all Functional Requirements:
Part A: Encapsulation, Properties, Special Methods, Password Hashing
Part B: Inheritance, Super(), Overridden Methods, Runtime Polymorphism
Part C: Custom Exception Handling & Validation
Part D: Modules & Packages
Part E: JSON Persistence, CSV Export, Multithreaded Logging, Lockout Policy
"""

import os
import sys
import time

# Ensure root directory is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from secure_system import (
    User,
    Administrator,
    SecurityAnalyst,
    Validator,
    SecurityUtils,
    MultithreadedLogger,
    DataManager,
    UserManagementException,
    InvalidEmailException,
    WeakPasswordException,
    InvalidUserIDException,
    AuthenticationFailedException,
    AccountLockedException,
)

def print_header(title: str):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def main():
    print_header("CYBER SECURITY INSTITUTE - SECURE USER MANAGEMENT SYSTEM DEMO")
    
    # Initialize Multithreaded Logger
    logger = MultithreadedLogger("data/demo_activity_logs.txt")
    print("[+] Multithreaded Activity Logger initialized (Running on background thread).")

    # -------------------------------------------------------------------------
    # PART A & B: Class Design, Encapsulation, Inheritance & Polymorphism
    # -------------------------------------------------------------------------
    print_header("PART A & B: CREATING USERS & DEMONSTRATING OOP CONCEPTS")
    
    admin = Administrator(
        user_id="ADM-001",
        name="Dr. Sarah Connor",
        email="s.connor@cyberinstitute.edu",
        password="AdminP@ssword2026!",
        admin_level="SUPER_ADMIN",
        managed_departments=["Threat Intel", "System Ops", "Research"]
    )
    logger.log(admin.user_id, "REGISTER_USER", "SUCCESS", f"Created Administrator: {admin.name}")

    analyst_1 = SecurityAnalyst(
        user_id="ANA-101",
        name="Alex Mercer",
        email="a.mercer@cyberinstitute.edu",
        password="AnalystP@ss2026!",
        clearance_level="TOP_SECRET",
        assigned_incidents=["INC-9041", "INC-9042"]
    )
    logger.log(analyst_1.user_id, "REGISTER_USER", "SUCCESS", f"Created Security Analyst: {analyst_1.name}")

    analyst_2 = SecurityAnalyst(
        user_id="ANA-102",
        name="Elena Rostova",
        email="e.rostova@cyberinstitute.edu",
        password="CyberP@ssword2026!",
        clearance_level="SECRET",
        assigned_incidents=["INC-9043"]
    )
    logger.log(analyst_2.user_id, "REGISTER_USER", "SUCCESS", f"Created Security Analyst: {analyst_2.name}")

    user_list: list[User] = [admin, analyst_1, analyst_2]

    print("[*] Encapsulation & Special Methods Demo:")
    for user in user_list:
        print(f"    - __str__()  : {str(user)}")
        print(f"    - __repr__() : {repr(user)}")

    print("\n[*] Runtime Polymorphism Demo (Iterating through User references):")
    for u in user_list:
        print(f"\n    [+] User ID: {u.user_id} | Class: {u.__class__.__name__}")
        print(f"        Role Privileges Count: {len(u.get_privileges())}")
        print(f"        Privilege List       : {u.get_privileges()}")
        print(f"        Polymorphic Task Output: {u.execute_role_task()}")

    # -------------------------------------------------------------------------
    # PART C: Exception Handling & Input Validation
    # -------------------------------------------------------------------------
    print_header("PART C: EXCEPTION HANDLING & INPUT VALIDATION DEMO")
    
    test_cases = [
        ("Invalid Email", lambda: Validator.validate_email("bad_email.com")),
        ("Weak Password", lambda: Validator.validate_password_strength("simple123")),
        ("Invalid User ID", lambda: Validator.validate_user_id("USER_123_INVALID")),
    ]

    for label, fn in test_cases:
        try:
            print(f"[*] Testing {label} validation...")
            fn()
        except UserManagementException as ex:
            print(f"    [EXPECTED EXCEPTION CAUGHT] Code: {ex.code} | Message: {ex.message}")
            logger.log("SYSTEM", "VALIDATION_TEST", "FAILURE", f"Caught expected exception: {ex.code}")
        else:
            print("    [WARNING] Expected exception was not raised.")

    # -------------------------------------------------------------------------
    # PART E: Password Strength Checker & Account Lockout Tracker
    # -------------------------------------------------------------------------
    print_header("PART E: PASSWORD STRENGTH CHECKER & LOGIN LOCKOUT POLICY")
    
    passwords_to_test = ["12345", "cyberpass", "CyberP@ss2026!", "P@ssw0rdSuper123!#"]
    print("[*] Password Strength Evaluator Tool:")
    for p in passwords_to_test:
        eval_result = SecurityUtils.evaluate_password_score(p)
        print(f"    - Password: '{p:<20}' -> Score: {eval_result['score']}/100 | Rating: {eval_result['rating']}")

    print("\n[*] Testing Account Lockout Policy (3 Failed Attempts):")
    test_user = SecurityAnalyst("ANA-999", "Test Target", "target@cyberinstitute.edu", "TargetP@ss123!")
    
    for attempt in range(1, 4):
        try:
            print(f"    Attempt {attempt}: Attempting login with incorrect password...")
            test_user.authenticate("WrongPassword!")
        except AccountLockedException as locked_ex:
            print(f"    [ACCOUNT LOCKED] {locked_ex}")
            logger.log(test_user.user_id, "LOGIN_ATTEMPT", "LOCKED", f"Account locked after attempt {attempt}")
        except AuthenticationFailedException as auth_ex:
            print(f"    [AUTH FAILED] {auth_ex}")
            logger.log(test_user.user_id, "LOGIN_ATTEMPT", "FAILURE", f"Failed attempt {attempt}")

    print(f"    Current Account Lock Status: is_locked = {test_user.is_locked}")
    
    print("\n[*] Unlocking Account via Administrator Authorization:")
    unlock_msg = admin.unlock_user(test_user)
    print(f"    {unlock_msg}")
    print(f"    Post-Unlock Status: is_locked = {test_user.is_locked}")
    print(f"    Authenticating with correct password...")
    test_user.authenticate("TargetP@ss123!")
    print("    [SUCCESS] Authentication succeeded after unlocking!")
    logger.log(test_user.user_id, "LOGIN_ATTEMPT", "SUCCESS", "Authenticated successfully after admin unlock.")

    # -------------------------------------------------------------------------
    # PART E: Data Persistence, CSV Export & Multithreaded Logging
    # -------------------------------------------------------------------------
    print_header("PART E: DATA PERSISTENCE, CSV EXPORT & REPORT GENERATION")

    # 1. JSON Persistence
    json_file = "data/users.json"
    print(f"[*] Saving {len(user_list)} polymorphic users to JSON repository ({json_file})...")
    DataManager.save_users_to_json(user_list, json_file)
    print("    [SUCCESS] Users saved to JSON.")

    print(f"[*] Re-loading users from JSON file to verify state restoration...")
    reloaded_users = DataManager.load_users_from_json(json_file)
    print(f"    [SUCCESS] Loaded {len(reloaded_users)} users from disk:")
    for ru in reloaded_users:
        print(f"      - ID: {ru.user_id:<8} | Class: {ru.__class__.__name__:<18} | Email: {ru.email}")

    # 2. CSV Export
    csv_file = "data/user_directory.csv"
    print(f"\n[*] Exporting user directory to CSV file ({csv_file})...")
    DataManager.export_users_to_csv(reloaded_users, csv_file)
    print("    [SUCCESS] User directory exported to CSV.")

    # 3. Multithreaded Activity Log & Report Generation
    print("\n[*] Waiting for background logging thread to sync entries...")
    time.sleep(1.0)
    logger.shutdown()
    print("    [SUCCESS] Multithreaded logging worker thread cleanly joined.")

    logs = logger.get_logs()
    print(f"    Total Log Entries Processed Asynchronously: {len(logs)}")
    
    report_file = "data/activity_summary_report.txt"
    print(f"[*] Generating System Activity Audit Report ({report_file})...")
    report = DataManager.generate_activity_report(logs, report_file)
    
    print("\n--- SAMPLE AUDIT REPORT PREVIEW ---")
    print("\n".join(report.splitlines()[:15]))
    print("--- END PREVIEW ---")

    print_header("DEMONSTRATION COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    main()
