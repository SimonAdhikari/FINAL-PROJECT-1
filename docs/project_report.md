# COMPREHENSIVE TECHNICAL PROJECT REPORT

## PROJECT TITLE: Secure User Management System in Python Using Object-Oriented Programming

**Institution**: Cyber Security Institute  
**Course Module**: Advanced Object-Oriented Programming (OOP) & System Design  
**Language**: Python 3.10+  
**Date**: September 2026  
**Status**: Fully Implemented, Tested, and Verified  

---

## EXECUTIVE SUMMARY / ABSTRACT

The modern cyber security landscape demands robust user access control, strict privilege isolation, credential protection, and non-repudiable activity tracking. This technical report details the design, architecture, implementation, and verification of a production-grade **Secure User Management System** developed in Python using Object-Oriented Programming (OOP) paradigms.

The system addresses the core requirements of a Cyber Security Institute by providing role-based user management for **Administrators** and **Security Analysts**. Key achievements of this implementation include:
1. **Encapsulation & Cryptographic Security**: Restricting direct access to sensitive credentials by storing salted PBKDF2 HMAC-SHA256 password hashes instead of plain text, mediated through Python property decorators (`@property`).
2. **Inheritance & Runtime Polymorphism**: Building an extensible class hierarchy with abstract base class `User` and concrete subclasses `Administrator` and `SecurityAnalyst` that override operational tasks, privilege definitions, and dashboard reporting routines dynamically.
3. **Custom Exception Taxonomy**: Implementing a custom exception hierarchy extending `UserManagementException` to deliver granular input validation (`InvalidEmailException`, `WeakPasswordException`, `InvalidUserIDException`) and security policy enforcement (`AccountLockedException`, `AuthenticationFailedException`).
4. **Package & Modular Design**: Structuring the application cleanly into specialized sub-packages (`users`, `exceptions`, `utilities`, `storage`) promoting separation of concerns.
5. **Advanced Multithreaded Logging & Data Persistence**: Utilizing background worker threads (`threading.Thread`) and thread-safe queues (`queue.Queue`) for non-blocking activity logging, paired with JSON state persistence and CSV export capabilities.

---

## 1. INTRODUCTION & PROBLEM STATEMENT

### 1.1 Context and Background
Educational and research institutions in the cyber security domain handle sensitive information, security vulnerability feeds, and administrative infrastructure. Software systems operating within such environments must strictly enforce authentication, authorization, and accountability.

A common failure in legacy user management systems is the improper handling of credentials, monolithic source code organization, lack of input validation, and synchronous file logging that blocks execution during high-throughput operations.

### 1.2 Problem Statement
The Cyber Security Institute requires a specialized user management system capable of:
- Storing user metadata (User ID, Full Name, Email, Role, Cryptographic Credentials).
- Preventing unauthorized direct access to sensitive variables (Passwords and Salts).
- Supporting distinct role privileges for Administrators and Security Analysts.
- Validating all user input fields against strict security criteria and raising custom exceptions on failure.
- Organizing source code into clean Python modules and packages.
- Tracking and logging user operations asynchronously without compromising system responsiveness.

---

## 2. SYSTEM REQUIREMENTS & SPECIFICATIONS

### 2.1 Functional Requirements Checklist

| Requirement ID | Category | Requirement Description | Implementation Status |
|---|---|---|---|
| **FR-A1** | Encapsulation | Private object attributes for sensitive fields (`__user_id`, `__email`, `__password_hash`, `__salt`). | **COMPLETED** |
| **FR-A2** | Encapsulation | Property getters and validated setters using `@property` decorators. | **COMPLETED** |
| **FR-A3** | Special Methods | Override special dunder methods: `__str__()`, `__repr__()`, `__eq__()`. | **COMPLETED** |
| **FR-B1** | Inheritance | Base class `User` and derived classes `Administrator` and `SecurityAnalyst`. | **COMPLETED** |
| **FR-B2** | Polymorphism | Runtime polymorphic invocation of `get_privileges()`, `execute_role_task()`, and `generate_dashboard_summary()`. | **COMPLETED** |
| **FR-B3** | Super Function | Proper initialization of parent class attributes using `super().__init__()`. | **COMPLETED** |
| **FR-C1** | Exceptions | Custom exception hierarchy inheriting from `UserManagementException`. | **COMPLETED** |
| **FR-C2** | Validation | Input validation routines for email RFC formatting, User ID patterns, and password strength. | **COMPLETED** |
| **FR-C3** | Exception Blocks | Comprehensive `try-except-else-finally-raise` control flows. | **COMPLETED** |
| **FR-D1** | Modules | Clean Python package organization (`secure_system/users`, `exceptions`, `utilities`, `storage`). | **COMPLETED** |
| **FR-E1** | Persistence | JSON file saving/loading preserving polymorphic object state. | **COMPLETED** |
| **FR-E2** | Data Export | CSV directory export and structured activity summary report generation. | **COMPLETED** |
| **FR-E3** | Multithreading | Thread-safe background activity logger using `threading.Thread` and `queue.Queue`. | **COMPLETED** |
| **FR-E4** | Security Feature | Password strength scoring engine and Account Lockout policy after 3 failed logins. | **COMPLETED** |

---

## 3. OBJECT-ORIENTED ARCHITECTURE & DESIGN

### 3.1 Encapsulation and Data Hiding (Part A)
In Python, attributes prefixed with double underscores (`__attribute`) trigger name mangling, rendering them private to the class scope. The `User` base class leverages this mechanism to protect sensitive fields:

```python
class User(ABC):
    def __init__(self, user_id: str, name: str, email: str, password: str, role: str):
        self.__user_id = Validator.validate_user_id(user_id)
        self.__name = Validator.validate_name(name)
        self.__email = Validator.validate_email(email)
        self.__role = role
        
        # Salted PBKDF2 Hashing
        self.__salt = SecurityUtils.generate_salt()
        self.__password_hash = SecurityUtils.hash_password(password, self.__salt)
        
        self.__is_active = True
        self.__failed_login_attempts = 0
        self.__is_locked = False
```

Direct access to `user.__password_hash` raises an `AttributeError`. Access is strictly controlled via property decorators:

```python
@property
def name(self) -> str:
    return self.__name

@name.setter
def name(self, new_name: str):
    self.__name = Validator.validate_name(new_name)
```

#### Cryptographic Security Model
Passwords are never stored in plain text. When a user registers or changes their password:
1. A unique 16-byte random salt is generated via `secrets.token_hex(16)`.
2. The password is key-stretched using **PBKDF2-HMAC-SHA256** with 100,000 iterations.
3. Verification employs constant-time string comparison (`hmac.compare_digest`) to prevent timing side-channel attacks.

### 3.2 Inheritance Hierarchy and Runtime Polymorphism (Part B)
Inheritance allows specialized roles to extend core user capabilities while sharing a unified interface.

```
                  +--------------------------------+
                  |         <<Abstract>>           |
                  |             User               |
                  +--------------------------------+
                  | - __user_id: str               |
                  | - __password_hash: str         |
                  | - __salt: str                  |
                  +--------------------------------+
                  | + authenticate(password) bool  |
                  | + get_privileges()* list       |
                  | + execute_role_task()* str     |
                  +--------------------------------+
                                  ^
                                  |
            +---------------------+---------------------+
            |                                           |
+------------------------+                 +------------------------+
|     Administrator      |                 |     SecurityAnalyst    |
+------------------------+                 +------------------------+
| - __admin_level: str   |                 | - __clearance: str     |
| - __departments: list  |                 | - __incidents: list    |
+------------------------+                 +------------------------+
| + lock_user()          |                 | + conduct_scan()       |
| + unlock_user()        |                 | + assign_incident()    |
| + get_privileges()     |                 | + get_privileges()     |
| + execute_role_task()  |                 | + execute_role_task()  |
+------------------------+                 +------------------------+
```

#### Utilizing `super()`
Child class constructors invoke `super().__init__()` to initialize base attributes before adding role-specific attributes:

```python
class Administrator(User):
    def __init__(self, user_id, name, email, password, admin_level="SUPER_ADMIN", managed_departments=None):
        super().__init__(user_id=user_id, name=name, email=email, password=password, role="Administrator")
        self.__admin_level = admin_level
        self.__managed_departments = managed_departments or ["IT Operations", "Cyber Security"]
```

#### Polymorphic Dispatch
Polymorphism allows the system controller to operate on instances of `User` without knowing their exact subclass type at compile time:

```python
users: list[User] = [admin_obj, analyst_obj]

for u in users:
    # Dynamically dispatches to Administrator.execute_role_task() or SecurityAnalyst.execute_role_task()
    print(u.execute_role_task())
```

---

## 4. EXCEPTION HANDLING & INPUT VALIDATION (Part C)

### 4.1 Custom Exception Taxonomy
The system implements a specialized exception hierarchy rooted at `UserManagementException`:

```
UserManagementException (Base Exception)
 ├── InvalidEmailException
 ├── WeakPasswordException
 ├── InvalidUserIDException
 ├── AuthenticationFailedException
 │    └── AccountLockedException
 ├── PermissionDeniedException
 ├── UserAlreadyExistsException
 └── UserNotFoundException
```

### 4.2 Validation Logic
Input validation is encapsulated in `secure_system.utilities.Validator`:

1. **Email Validation**: Enforces RFC 5322 pattern (`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`).
2. **User ID Validation**: Enforces strict institute pattern (`^[A-Z]{3}-\d{3,6}$`), e.g., `ADM-001`, `ANA-101`.
3. **Password Strength Rules**:
   - Minimum length: 8 characters
   - At least 1 uppercase letter (`[A-Z]`)
   - At least 1 lowercase letter (`[a-z]`)
   - At least 1 digit (`\d`)
   - At least 1 special symbol (`[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]`)

If any constraint fails, `Validator` raises the corresponding custom exception containing detailed failure reasons.

---

## 5. ADVANCED FEATURES IMPLEMENTATION (Part E)

### 5.1 Multithreaded Activity Logger
Logging system events synchronously to disk can introduce file I/O latency. To eliminate this bottleneck, `MultithreadedLogger` implements an asynchronous **Producer-Consumer pattern**:

- **Producer**: Main application thread calls `logger.log(user_id, action, status, details)`, placing log records into a thread-safe `queue.Queue`.
- **Consumer**: A dedicated background thread (`daemon=True`) continuously pulls items from the queue and writes them to `data/activity_logs.txt`.

```python
class MultithreadedLogger:
    def _process_logs(self):
        while self.is_running or not self.log_queue.empty():
            try:
                entry = self.log_queue.get(timeout=0.5)
                if entry is None:
                    break
                with open(self.log_file_path, "a", encoding="utf-8") as f:
                    f.write(entry + "\n")
                self.log_queue.task_done()
            except queue.Empty:
                continue
```

### 5.2 Password Strength Evaluator Tool
`SecurityUtils.evaluate_password_score(password)` analyzes password complexity and returns:
- A numerical score from 0 to 100%.
- A qualitative rating (`WEAK`, `MODERATE`, `STRONG`, `VERY STRONG`).
- Specific actionable recommendations to improve password strength.

### 5.3 Login Attempt Tracker & Account Lockout Policy
To counter brute-force authentication attacks, the `User` base class tracks consecutive failed login attempts (`__failed_login_attempts`):
- Each authentication failure increments the counter.
- When `__failed_login_attempts >= 3`, the account status is updated to `__is_locked = True`, and an `AccountLockedException` is raised.
- Locked accounts cannot authenticate until an `Administrator` explicitly invokes `unlock_user(target_user)`.

### 5.4 JSON Persistence & CSV Export
- **JSON Serialization**: `DataManager.save_users_to_json()` converts user object graphs into JSON format while preserving polymorphic type tags (`"class": "Administrator"`).
- **JSON Deserialization**: `DataManager.load_users_from_json()` reads stored records and instantiates the correct concrete classes (`Administrator` or `SecurityAnalyst`), restoring exact security flags, salts, and password hashes.
- **CSV Directory Export**: `DataManager.export_users_to_csv()` outputs a clean user roster suitable for auditing and reporting.

---

## 6. PROJECT PACKAGE STRUCTURE (Part D)

The project adheres to professional Python package layout:

```
FINAL PROJECT 1/
│
├── secure_system/                  # Root Package
│   ├── __init__.py                 # Export initialization
│   │
│   ├── exceptions/                 # Exception Package
│   │   ├── __init__.py
│   │   └── custom_exceptions.py    # Custom Exception Classes
│   │
│   ├── utilities/                  # Utilities Package
│   │   ├── __init__.py
│   │   ├── validator.py            # Input Validation
│   │   ├── security.py             # PBKDF2 Hashing & Password Score
│   │   └── logger.py               # Multithreaded Async Logger
│   │
│   ├── users/                      # Domain Model Package
│   │   ├── __init__.py
│   │   ├── user.py                 # Base User Class
│   │   ├── administrator.py        # Administrator Class
│   │   └── analyst.py              # SecurityAnalyst Class
│   │
│   └── storage/                    # Persistence Package
│       ├── __init__.py
│       └── persistence.py          # DataManager (JSON / CSV / Reports)
│
├── tests/                          # Test Suite
│   └── test_system.py              # Pytest/Unittest Automation
│
├── data/                           # Runtime Storage Folder
│   ├── users.json
│   ├── user_directory_export.csv
│   └── activity_logs.txt
│
├── docs/                           # Documentation Deliverables
│   ├── project_report.md           # 8-12 Page Project Report
│   ├── presentation_slides.md      # Presentation Slide Deck
│   └── uml_class_diagram.md        # Mermaid UML Diagrams
│
├── main.py                         # Interactive CLI Application
└── demo.py                         # End-to-End Automated Demonstration Runner
```

---

## 7. SYSTEM VERIFICATION & TEST RESULTS

### 7.1 Automated Unit Testing
The system was validated using Python's `unittest` framework in `tests/test_system.py`. Seven test suites were executed covering all core functionalities:

1. `test_01_user_encapsulation_and_properties`: Verified property accessors and data encapsulation.
2. `test_02_special_dunder_methods`: Verified `__str__`, `__repr__`, and `__eq__` equality logic.
3. `test_03_inheritance_and_polymorphism`: Verified polymorphic method dispatch across `Administrator` and `SecurityAnalyst`.
4. `test_04_custom_exception_handling`: Verified raising of `InvalidEmailException`, `WeakPasswordException`, and `InvalidUserIDException`.
5. `test_05_account_lockout_policy`: Verified lockout after 3 failed attempts and subsequent administrator unlock.
6. `test_06_data_persistence_and_export`: Verified JSON state saving/loading and CSV export.
7. `test_07_multithreaded_logger`: Verified background thread log processing.

```
Ran 7 tests in 1.458s

OK
```

### 7.2 End-to-End Demonstration Verification
The automated demonstration runner (`demo.py`) was executed to demonstrate the complete lifecycle of system operations:

- Created `Administrator` and `SecurityAnalyst` accounts.
- Executed polymorphic tasks.
- Successfully triggered and caught custom validation exceptions.
- Evaluated password strength metrics.
- Simulated account lockout on 3 failed login attempts and demonstrated administrator unlock.
- Saved user repository to JSON, reloaded state, exported CSV directory, and generated a formatted audit log report.

---

## 8. CONCLUSION & FUTURE ENHANCEMENTS

### 8.1 Conclusion
The **Secure User Management System** successfully fulfills all functional requirements set forth by the Cyber Security Institute. By combining Object-Oriented Programming principles (**Encapsulation**, **Inheritance**, **Polymorphism**, **Modularity**) with cyber security best practices (**Salted PBKDF2 Hashing**, **Account Lockout Rules**, **Custom Exception Handling**, and **Asynchronous Multithreaded Logging**), the system provides a robust, scalable, and maintainable solution.

### 8.2 Future Enhancements
Potential future extensions for the project include:
1. **Role-Based Access Control (RBAC) Decorators**: Implementing custom Python decorators to enforce permission checks automatically on method calls.
2. **Multi-Factor Authentication (MFA)**: Integrating Time-based One-Time Passwords (TOTP) using standard RFC 6238 algorithms.
3. **Database Integration**: Replacing JSON storage with an ORM framework such as SQLAlchemy connected to PostgreSQL/SQLite.
