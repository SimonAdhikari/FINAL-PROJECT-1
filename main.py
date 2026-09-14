"""
Interactive Command-Line Interface (CLI) for Secure User Management System.

Allows administrators and security analysts to log in, manage users,
run security tasks, evaluate password strength, and export logs/data.
"""

import sys
import os

# Ensure package path is included
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
    AuthenticationFailedException,
    AccountLockedException,
)

DATA_JSON_PATH = "data/users.json"
DATA_CSV_PATH = "data/user_directory_export.csv"
LOG_FILE_PATH = "data/activity_logs.txt"

def initialize_default_users(data_manager: DataManager) -> list[User]:
    """Loads existing user repository or seeds default system accounts."""
    if os.path.exists(DATA_JSON_PATH):
        try:
            users = data_manager.load_users_from_json(DATA_JSON_PATH)
            if users:
                return users
        except Exception as e:
            print(f"[!] Warning: Could not load JSON repo ({e}). Initializing default accounts.")

    # Seed default accounts
    admin = Administrator(
        user_id="ADM-001",
        name="Chief Admin",
        email="admin@cyberinstitute.edu",
        password="AdminP@ssword2026!",
        admin_level="SUPER_ADMIN"
    )
    analyst = SecurityAnalyst(
        user_id="ANA-101",
        name="Lead Analyst",
        email="analyst@cyberinstitute.edu",
        password="AnalystP@ssword2026!",
        clearance_level="TOP_SECRET",
        assigned_incidents=["INC-1001", "INC-1002"]
    )
    users = [admin, analyst]
    data_manager.save_users_to_json(users, DATA_JSON_PATH)
    return users

class SecureUserManagementCLI:

    def __init__(self):
        self.logger = MultithreadedLogger(LOG_FILE_PATH)
        self.data_manager = DataManager()
        self.users = initialize_default_users(self.data_manager)
        self.current_user: User | None = None

    def save_state(self):
        self.data_manager.save_users_to_json(self.users, DATA_JSON_PATH)

    def find_user_by_id(self, user_id: str) -> User | None:
        user_id_clean = user_id.strip().upper()
        for u in self.users:
            if u.user_id == user_id_clean:
                return u
        return None

    def run(self):
        while True:
            print("\n" + "=" * 65)
            print("     CYBER SECURITY INSTITUTE - SECURE USER MANAGEMENT")
            print("=" * 65)
            print(" 1. Login to Account")
            print(" 2. Register New User Account")
            print(" 3. Password Strength Evaluator Tool")
            print(" 4. View System Activity Logs")
            print(" 5. Export User Directory to CSV")
            print(" 6. System Diagnostics & Info")
            print(" 7. Exit Application")
            print("-" * 65)

            choice = input("Select an option (1-7): ").strip()

            if choice == "1":
                self.login_flow()
            elif choice == "2":
                self.register_user_flow()
            elif choice == "3":
                self.password_checker_tool()
            elif choice == "4":
                self.view_activity_logs()
            elif choice == "5":
                self.export_csv_flow()
            elif choice == "6":
                self.system_info()
            elif choice == "7":
                print("\n[+] Saving state and shutting down Security System logger...")
                self.save_state()
                self.logger.shutdown()
                print("[+] Goodbye!")
                break
            else:
                print("[!] Invalid choice. Please select between 1 and 7.")

    def login_flow(self):
        print("\n--- ACCOUNT AUTHENTICATION ---")
        user_id = input("Enter User ID (e.g. ADM-001, ANA-101): ").strip()
        user = self.find_user_by_id(user_id)

        if not user:
            print(f"[!] User ID '{user_id}' not found in system.")
            self.logger.log("UNKNOWN", "LOGIN", "FAILURE", f"Non-existent User ID attempt: {user_id}")
            register_prompt = input("Would you like to register a new account now? (y/n): ").strip().lower()
            if register_prompt in ["y", "yes"]:
                self.register_user_flow()
            return

        password = input("Enter Password: ").strip()

        try:
            if user.authenticate(password):
                self.current_user = user
                print(f"\n[+] Authentication Successful! Welcome, {user.name} ({user.role}).")
                self.logger.log(user.user_id, "LOGIN", "SUCCESS", f"User authenticated: {user.name}")
                self.user_dashboard()
        except AccountLockedException as e:
            print(f"\n[ACCOUNT LOCKED] {e.message}")
            self.logger.log(user.user_id, "LOGIN", "LOCKED", "Login blocked due to locked status.")
        except AuthenticationFailedException as e:
            print(f"\n[AUTH ERROR] {e.message}")
            self.logger.log(user.user_id, "LOGIN", "FAILURE", e.message)
            self.save_state()

    def register_user_flow(self):
        print("\n--- NEW USER ACCOUNT REGISTRATION ---")
        print("Select Role Type:")
        print(" 1. Administrator (e.g. ADM-002)")
        print(" 2. Security Analyst (e.g. ANA-201)")
        role_type = input("Choice (1 or 2): ").strip()

        user_id = input("Enter User ID (e.g. ADM-002, ANA-201): ").strip()
        if self.find_user_by_id(user_id):
            print(f"[!] Registration Error: User ID '{user_id}' is already registered.")
            return

        name = input("Enter Full Name: ").strip()
        email = input("Enter Email Address: ").strip()
        password = input("Enter Password: ").strip()

        try:
            if role_type == "1":
                level = input("Admin Level (SUPER_ADMIN / SYSTEM_ADMIN) [Default: SUPER_ADMIN]: ").strip() or "SUPER_ADMIN"
                new_user = Administrator(user_id, name, email, password, admin_level=level)
            elif role_type == "2":
                clearance = input("Clearance Level (CONFIDENTIAL / SECRET / TOP_SECRET) [Default: SECRET]: ").strip() or "SECRET"
                new_user = SecurityAnalyst(user_id, name, email, password, clearance_level=clearance)
            else:
                print("[!] Invalid role choice. Registration cancelled.")
                return

            self.users.append(new_user)
            self.save_state()
            creator_id = self.current_user.user_id if self.current_user else "SELF_REGISTRATION"
            print(f"\n[+] Registration Successful! Account '{name}' ({user_id}) created.")
            self.logger.log(creator_id, "REGISTER_USER", "SUCCESS", f"Registered new user {user_id} ({new_user.role})")
        except UserManagementException as e:
            print(f"\n[!] Registration Failed: {e.message}")
            self.logger.log("SYSTEM", "REGISTER_USER", "FAILURE", e.message)

    def user_dashboard(self):
        while self.current_user:
            print("\n" + "=" * 65)
            print(f" DASHBOARD - Logged in as: {self.current_user.name} ({self.current_user.role})")
            print("=" * 65)
            print(" 1. View Account Profile & Privileges")
            print(" 2. Execute Primary Role Task")
            print(" 3. Change Account Password")

            if isinstance(self.current_user, Administrator):
                print(" 4. Create New User Account [Admin]")
                print(" 5. Lock / Unlock User Account [Admin]")
                print(" 6. View All System Users [Admin]")
            elif isinstance(self.current_user, SecurityAnalyst):
                print(" 4. Conduct Vulnerability Network Scan [Analyst]")
                print(" 5. Manage Assigned Incident Tickets [Analyst]")
                print(" 6. Inspect Threat Intelligence Feed [Analyst]")

            print(" 0. Logout")
            print("-" * 65)

            choice = input("Select Menu Option: ").strip()

            if choice == "0":
                print(f"[+] Logging out {self.current_user.name}...")
                self.logger.log(self.current_user.user_id, "LOGOUT", "SUCCESS", "User logged out.")
                self.current_user = None
                self.save_state()
                break
            elif choice == "1":
                self.view_profile()
            elif choice == "2":
                print(f"\n{self.current_user.execute_role_task()}")
                self.logger.log(self.current_user.user_id, "EXECUTE_TASK", "SUCCESS", "Role task executed.")
            elif choice == "3":
                self.change_password_flow()
            elif choice == "4":
                if isinstance(self.current_user, Administrator):
                    self.admin_create_user()
                elif isinstance(self.current_user, SecurityAnalyst):
                    self.analyst_run_scan()
            elif choice == "5":
                if isinstance(self.current_user, Administrator):
                    self.admin_lock_unlock_user()
                elif isinstance(self.current_user, SecurityAnalyst):
                    self.analyst_manage_incidents()
            elif choice == "6":
                if isinstance(self.current_user, Administrator):
                    self.list_all_users()
                elif isinstance(self.current_user, SecurityAnalyst):
                    print("\n[+] Threat Feed: All internal subnets clear. SIEM status: HEALTHY.")

    def view_profile(self):
        if not self.current_user:
            return
        print("\n--- ACCOUNT PROFILE ---")
        print(f" String Representation : {str(self.current_user)}")
        print(f" User ID               : {self.current_user.user_id}")
        print(f" Full Name             : {self.current_user.name}")
        print(f" Email                 : {self.current_user.email}")
        print(f" Account Role          : {self.current_user.role}")
        print(f" Account Active Status : {'Active' if self.current_user.is_active else 'Deactivated'}")
        print(f" Lockout Status        : {'LOCKED' if self.current_user.is_locked else 'Normal'}")
        print(f" Privileges ({len(self.current_user.get_privileges())})    : {', '.join(self.current_user.get_privileges())}")

    def change_password_flow(self):
        old_pass = input("Enter Current Password: ").strip()
        new_pass = input("Enter New Password: ").strip()
        try:
            self.current_user.change_password(old_pass, new_pass)
            print("[+] Password updated successfully!")
            self.logger.log(self.current_user.user_id, "CHANGE_PASSWORD", "SUCCESS", "Password updated.")
            self.save_state()
        except UserManagementException as e:
            print(f"[!] Password change failed: {e.message}")
            self.logger.log(self.current_user.user_id, "CHANGE_PASSWORD", "FAILURE", e.message)

    def admin_create_user(self):
        print("\n--- CREATE NEW USER ACCOUNT (ADMIN) ---")
        role_type = input("Select Role (1 = Administrator, 2 = Security Analyst): ").strip()
        user_id = input("Enter User ID (e.g. ADM-002, ANA-201): ").strip()
        name = input("Enter Full Name: ").strip()
        email = input("Enter Email Address: ").strip()
        password = input("Enter Password: ").strip()

        try:
            if role_type == "1":
                level = input("Admin Level (SUPER_ADMIN / SYSTEM_ADMIN) [Default: SUPER_ADMIN]: ").strip() or "SUPER_ADMIN"
                new_user = Administrator(user_id, name, email, password, admin_level=level)
            else:
                clearance = input("Clearance (SECRET / TOP_SECRET) [Default: SECRET]: ").strip() or "SECRET"
                new_user = SecurityAnalyst(user_id, name, email, password, clearance_level=clearance)

            if self.find_user_by_id(user_id):
                print(f"[!] Error: User ID '{user_id}' already exists.")
                return

            self.users.append(new_user)
            self.save_state()
            print(f"[+] User '{name}' ({user_id}) registered successfully!")
            self.logger.log(self.current_user.user_id, "CREATE_USER", "SUCCESS", f"Created user {user_id}")
        except UserManagementException as e:
            print(f"[!] Creation failed: {e.message}")

    def admin_lock_unlock_user(self):
        target_id = input("Enter User ID to lock/unlock: ").strip()
        target = self.find_user_by_id(target_id)
        if not target:
            print("[!] User not found.")
            return

        print(f"Target User: {target.name} | Current Status: locked={target.is_locked}")
        action = input("Type 'L' to Lock, 'U' to Unlock: ").strip().upper()
        if action == "L":
            msg = self.current_user.lock_user(target)
            print(f"[+] {msg}")
            self.logger.log(self.current_user.user_id, "LOCK_USER", "SUCCESS", f"Locked {target_id}")
        elif action == "U":
            msg = self.current_user.unlock_user(target)
            print(f"[+] {msg}")
            self.logger.log(self.current_user.user_id, "UNLOCK_USER", "SUCCESS", f"Unlocked {target_id}")
        self.save_state()

    def analyst_run_scan(self):
        target = input("Enter target network subnet [Default: 192.168.1.0/24]: ").strip() or "192.168.1.0/24"
        scan_results = self.current_user.conduct_vulnerability_scan(target)
        print("\n--- VULNERABILITY SCAN RESULTS ---")
        for k, v in scan_results.items():
            print(f" {k:<25}: {v}")
        self.logger.log(self.current_user.user_id, "VULN_SCAN", "SUCCESS", f"Scanned {target}")

    def analyst_manage_incidents(self):
        print(f"\nActive Assigned Tickets: {self.current_user.assigned_incidents}")
        ticket_id = input("Enter new Incident ID to assign (or press Enter to skip): ").strip()
        if ticket_id:
            self.current_user.assign_incident(ticket_id)
            print(f"[+] Assigned ticket '{ticket_id}'.")
            self.save_state()

    def list_all_users(self):
        print("\n--- SYSTEM USER DIRECTORY ---")
        for u in self.users:
            print(f" - {u}")

    def password_checker_tool(self):
        print("\n--- PASSWORD STRENGTH EVALUATOR TOOL ---")
        pwd = input("Enter password to test: ").strip()
        res = SecurityUtils.evaluate_password_score(pwd)
        print(f" Score: {res['score']}/100 | Rating: {res['rating']}")
        if res['feedback']:
            print(" Recommendations to improve:")
            for f in res['feedback']:
                print(f"   * {f}")

    def view_activity_logs(self):
        print("\n--- RECENT SYSTEM ACTIVITY AUDIT LOGS ---")
        logs = self.logger.get_logs()
        if not logs:
            print(" No logs recorded yet.")
        else:
            for line in logs[-15:]:
                print(f" {line}")

    def export_csv_flow(self):
        DataManager.export_users_to_csv(self.users, DATA_CSV_PATH)
        print(f"[+] User directory successfully exported to CSV: {DATA_CSV_PATH}")

    def system_info(self):
        print("\n--- SYSTEM ARCHITECTURE INFO ---")
        print(" Cyber Security Institute User Management System v1.0.0")
        print(f" Total Registered Users : {len(self.users)}")
        print(" Modules Loaded         : users, exceptions, utilities, storage")
        print(" Password Security      : Salted PBKDF2-HMAC-SHA256 (100,000 iterations)")
        print(" Multithreading Logger  : ACTIVE (queue.Queue + daemon Thread)")

if __name__ == "__main__":
    app = SecureUserManagementCLI()
    app.run()
