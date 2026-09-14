# UML Class Diagram Documentation

## System Architectural Class Diagram

The following Mermaid diagram illustrates the class hierarchy, inheritance relationships, encapsulation access modifiers (`-` private, `+` public, `#` protected), association, and utility dependencies in the Secure User Management System.

```mermaid
classDiagram
    %% Inheritance & Core Domain Classes
    class User {
        <<Abstract>>
        -str __user_id
        -str __name
        -str __email
        -str __role
        -str __password_hash
        -str __salt
        -bool __is_active
        -int __failed_login_attempts
        -bool __is_locked
        -str __created_at
        -str __last_login
        +user_id str
        +name str
        +email str
        +role str
        +is_active bool
        +is_locked bool
        +failed_login_attempts int
        +created_at str
        +last_login str
        +authenticate(password: str) bool
        +change_password(old_pass: str, new_pass: str) bool
        +lock_account() void
        +unlock_account() void
        +deactivate_account() void
        +activate_account() void
        +get_privileges()* list~str~
        +execute_role_task()* str
        +generate_dashboard_summary() dict
        +__str__() str
        +__repr__() str
        +__eq__(other: object) bool
    }

    class Administrator {
        -str __admin_level
        -list~str~ __managed_departments
        +admin_level str
        +managed_departments list~str~
        +add_department(dept: str) void
        +get_privileges() list~str~
        +execute_role_task() str
        +generate_dashboard_summary() dict
        +lock_user(target_user: User) str
        +unlock_user(target_user: User) str
        +__str__() str
    }

    class SecurityAnalyst {
        -str __clearance_level
        -list~str~ __assigned_incidents
        +clearance_level str
        +assigned_incidents list~str~
        +assign_incident(incident_id: str) void
        +resolve_incident(incident_id: str) bool
        +get_privileges() list~str~
        +execute_role_task() str
        +generate_dashboard_summary() dict
        +conduct_vulnerability_scan(target: str) dict
        +__str__() str
    }

    User <|-- Administrator : Inherits
    User <|-- SecurityAnalyst : Inherits

    %% Utility & Security Classes
    class Validator {
        +EMAIL_REGEX Pattern
        +USER_ID_REGEX Pattern
        +validate_email(email: str)$ str
        +validate_user_id(user_id: str)$ str
        +validate_password_strength(password: str)$ str
        +validate_name(name: str)$ str
    }

    class SecurityUtils {
        +ITERATIONS int
        +generate_salt()$ str
        +hash_password(password: str, salt: str)$ str
        +verify_password(password: str, hash: str, salt: str)$ bool
        +evaluate_password_score(password: str)$ dict
    }

    class MultithreadedLogger {
        -_instance MultithreadedLogger
        -_lock Lock
        +str log_file_path
        +Queue log_queue
        +Thread worker_thread
        +bool is_running
        +log(user_id: str, action: str, status: str, details: str) void
        +shutdown() void
        +get_logs() list~str~
    }

    class DataManager {
        +save_users_to_json(users: list~User~, file_path: str)$ void
        +load_users_from_json(file_path: str)$ list~User~
        +export_users_to_csv(users: list~User~, csv_path: str)$ void
        +generate_activity_report(log_entries: list~str~, report_path: str)$ str
    }

    %% Custom Exception Hierarchy
    class UserManagementException {
        +str message
        +str code
        +__str__() str
    }

    class InvalidEmailException {
        +str email
    }

    class WeakPasswordException {
        +list~str~ reasons
    }

    class InvalidUserIDException {
        +str user_id
    }

    class AuthenticationFailedException {
    }

    class AccountLockedException {
    }

    UserManagementException <|-- InvalidEmailException
    UserManagementException <|-- WeakPasswordException
    UserManagementException <|-- InvalidUserIDException
    UserManagementException <|-- AuthenticationFailedException
    AuthenticationFailedException <|-- AccountLockedException

    %% Relationships
    User ..> Validator : Uses
    User ..> SecurityUtils : Uses
    Administrator ..> User : Manages
    DataManager ..> User : Serializes / Deserializes
    MultithreadedLogger ..> User : Logs Activities
```

## Class Relationship Descriptions

1. **Inheritance (`User` -> `Administrator`, `SecurityAnalyst`)**:
   - `Administrator` and `SecurityAnalyst` extend the base `User` class via `super().__init__()`.
   - Polymorphic method overriding is applied on `get_privileges()`, `execute_role_task()`, and `generate_dashboard_summary()`.

2. **Encapsulation**:
   - Attributes prefixed with `__` are strictly private to prevent direct access to sensitive credentials (`__password_hash`, `__salt`) or internal flags (`__failed_login_attempts`, `__is_locked`).
   - Access is mediated through public `@property` getters and validated setters.

3. **Exception Handling**:
   - `UserManagementException` forms the root of a specialized custom exception hierarchy.

4. **Utilities & Multithreading**:
   - `Validator` enforces regular expression rules.
   - `SecurityUtils` performs salted PBKDF2 HMAC SHA-256 hashing.
   - `MultithreadedLogger` runs a background consumer thread processing an asynchronous `queue.Queue`.
   - `DataManager` handles JSON state persistence and CSV report generation.
