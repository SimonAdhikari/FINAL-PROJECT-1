"""
Script to generate a professional PowerPoint presentation (.pptx)
explaining the Secure User Management System codebase, tools, and OOP architecture.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Define Color Palette (Modern Dark / Cyber Security Theme)
BG_COLOR = RGBColor(15, 23, 42)       # Slate 900 #0F172A
CARD_BG = RGBColor(30, 41, 59)        # Slate 800 #1E293B
PRIMARY_ACCENT = RGBColor(56, 189, 248) # Sky 400 #38BDF8
SECONDARY_ACCENT = RGBColor(168, 85, 247) # Purple 500 #A855F7
SUCCESS_COLOR = RGBColor(74, 222, 128)  # Green 400 #4ADE80
WARNING_COLOR = RGBColor(251, 146, 60) # Orange 400 #FB923C
TEXT_PRIMARY = RGBColor(248, 250, 252)  # Slate 50 #F8FAFC
TEXT_MUTED = RGBColor(148, 163, 184)    # Slate 400 #94A3B8

def add_slide_background(slide, prs):
    """Fills slide background with dark slate color."""
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = BG_COLOR
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title_text, category_text="CYBER SECURITY INSTITUTE"):
    """Adds a standard slide header banner."""
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.4))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = PRIMARY_ACCENT
    p_cat.font.name = "Arial"

    # Title text
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_PRIMARY
    p_title.font.name = "Arial"

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=None):
    """Creates a styled card container shape."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()
    return card

def build_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide1, prs)

    # Decorative background card
    add_card(slide1, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1), border_color=PRIMARY_ACCENT)

    tb = slide1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.333), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "CYBER SECURITY INSTITUTE"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = PRIMARY_ACCENT
    p0.space_after = Pt(15)

    p1 = tf.add_paragraph()
    p1.text = "Secure User Management System"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_PRIMARY
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Object-Oriented Programming (OOP) in Python: Architecture, Security, Tools & Codebase"
    p2.font.size = Pt(18)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_after = Pt(35)

    p3 = tf.add_paragraph()
    p3.text = "Author: Software Engineering & Cyber Security Team  |  Language: Python 3.10+"
    p3.font.size = Pt(13)
    p3.font.color.rgb = SUCCESS_COLOR

    # =========================================================================
    # SLIDE 2: EXECUTIVE OVERVIEW & PROBLEM STATEMENT
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide2, prs)
    add_header(slide2, "1. Executive Overview & Problem Statement")

    # Card 1: Problem Statement
    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=WARNING_COLOR)
    tb1 = slide2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "The Cyber Security Challenge"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WARNING_COLOR
    p.space_after = Pt(14)

    bullets1 = [
        "Cyber Security Institutes manage distinct personas (Administrators, Security Analysts) with varying access levels.",
        "Legacy user systems store credentials insecurely, lack robust validation, and log events synchronously.",
        "Synchronous disk logging blocks user workflows and lowers application responsiveness.",
        "Lack of proper encapsulation exposes sensitive password hashes to unauthorized internal modification."
    ]
    for b in bullets1:
        p_b = tf1.add_paragraph()
        p_b.text = f"•  {b}"
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(10)

    # Card 2: System Objectives
    add_card(slide2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2), border_color=SUCCESS_COLOR)
    tb2 = slide2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "Project Objectives & Solutions"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_COLOR
    p.space_after = Pt(14)

    bullets2 = [
        "Encapsulate Credentials: Protect passwords using salted PBKDF2 HMAC-SHA256 cryptographic hashing.",
        "Role Hierarchy: Use OOP inheritance for Administrator and SecurityAnalyst classes.",
        "Custom Exceptions: Validate inputs (Email, User ID, Password) and raise custom error types.",
        "Multithreaded Logging: Record activities asynchronously using daemon worker threads & queue.Queue.",
        "JSON/CSV Persistence: Store polymorphic user state and generate audit directory exports."
    ]
    for b in bullets2:
        p_b = tf2.add_paragraph()
        p_b.text = f"✓  {b}"
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: TECHNOLOGIES & TOOLS USED
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide3, prs)
    add_header(slide3, "2. Technologies & Standard Library Tools Used")

    tools = [
        ("Cryptographic Security", "hashlib & secrets", "Implements salted PBKDF2-HMAC-SHA256 hashing (100,000 iterations) and cryptographically secure random salt generation.", PRIMARY_ACCENT),
        ("Asynchronous Multithreading", "threading & queue", "Implements a producer-consumer background logging thread (daemon=True) for non-blocking file I/O audit tracking.", SECONDARY_ACCENT),
        ("Validation & Regular Expressions", "re & abc", "Enforces RFC email patterns, uppercase User ID patterns, and Abstract Base Class (ABC) interface enforcement.", SUCCESS_COLOR),
        ("Data Persistence & Export", "json & csv", "Provides polymorphic object graph serialization to JSON and automated user directory export to CSV format.", WARNING_COLOR),
        ("Automated Test Suite", "unittest", "Automates 7 comprehensive unit test suites covering encapsulation, inheritance, exception handling, and threading.", PRIMARY_ACCENT)
    ]

    top_pos = 1.6
    for title, module, desc, color in tools:
        add_card(slide3, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.95), border_color=color)
        tb = slide3.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.08), Inches(11.333), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = f"{title}  |  Module: "
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = TEXT_PRIMARY

        # Add inline colored module name
        run = p0.add_run()
        run.text = module
        run.font.bold = True
        run.font.color.rgb = color

        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(12)
        p1.font.color.rgb = TEXT_MUTED

        top_pos += 1.08

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & PACKAGE LAYOUT
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide4, prs)
    add_header(slide4, "3. Modular Package Architecture & Structure")

    # Column 1: Package Tree Text
    add_card(slide4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=PRIMARY_ACCENT)
    tb_tree = slide4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_tree = tb_tree.text_frame
    tf_tree.word_wrap = True

    p = tf_tree.paragraphs[0]
    p.text = "Package Layout (secure_system/)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_ACCENT
    p.space_after = Pt(10)

    tree_str = """secure_system/
├── exceptions/
│   └── custom_exceptions.py  # Error hierarchy
├── utilities/
│   ├── validator.py          # Input regex validation
│   ├── security.py           # PBKDF2 hashing & score
│   └── logger.py             # Multithreaded logger
├── users/
│   ├── user.py               # Abstract Base User
│   ├── administrator.py      # Admin role class
│   └── analyst.py            # Security Analyst class
└── storage/
    └── persistence.py        # JSON & CSV DataManager"""

    p_code = tf_tree.add_paragraph()
    p_code.text = tree_str
    p_code.font.name = "Consolas"
    p_code.font.size = Pt(11)
    p_code.font.color.rgb = SUCCESS_COLOR

    # Column 2: Package Responsibility Descriptions
    add_card(slide4, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb_desc = slide4.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_desc = tb_desc.text_frame
    tf_desc.word_wrap = True

    p = tf_desc.paragraphs[0]
    p.text = "Architectural Benefits"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p.space_after = Pt(12)

    packages_info = [
        ("Separation of Concerns", "Decouples validation, cryptographic operations, role logic, and file storage into independent packages."),
        ("High Reusability", "Utilities and exceptions can be reused across external CLI, Web API, or GUI interfaces without modification."),
        ("Maintainability", "Clean package initialization via __init__.py files providing unified module exports."),
        ("Scalability", "New roles (e.g. GuestUser, IncidentManager) can be added cleanly under users/ without breaking existing logic.")
    ]
    for title, detail in packages_info:
        p_t = tf_desc.add_paragraph()
        p_t.text = f"•  {title}: "
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = PRIMARY_ACCENT

        run = p_t.add_run()
        run.text = detail
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p_t.space_after = Pt(8)

    # =========================================================================
    # SLIDE 5: PART A - CLASS DESIGN & ENCAPSULATION
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide5, prs)
    add_header(slide5, "4. Part A: Class Design & Encapsulation")

    # Card 1: Encapsulation Mechanics
    add_card(slide5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=PRIMARY_ACCENT)
    tb_enc = slide5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_enc = tb_enc.text_frame
    tf_enc.word_wrap = True

    p = tf_enc.paragraphs[0]
    p.text = "Data Hiding & Security Model"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_ACCENT
    p.space_after = Pt(12)

    enc_bullets = [
        "Double Underscore Mangling: Attributes like __user_id, __password_hash, and __salt are private to class User scope.",
        "Property Decorators: Controlled getter access via @property and validated setter modification.",
        "Salted PBKDF2 Hashing: Plaintext passwords are never stored. Passwords are salted (16-byte random hex) and hashed with 100,000 PBKDF2 iterations.",
        "Constant-Time Verification: Verification uses hmac.compare_digest() to prevent timing side-channel attacks.",
        "Special Method Overrides: Custom implementations of __str__(), __repr__(), and __eq__() for clean object string representation."
    ]
    for b in enc_bullets:
        p_b = tf_enc.add_paragraph()
        p_b.text = f"•  {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(8)

    # Card 2: Code Snippet
    add_card(slide5, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb_code = slide5.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_code = tb_code.text_frame
    tf_code.word_wrap = True

    p = tf_code.paragraphs[0]
    p.text = "Encapsulation Code Snippet (user.py)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_COLOR
    p.space_after = Pt(10)

    snippet_enc = """class User(ABC):
    def __init__(self, user_id, name, email, password):
        self.__user_id = Validator.validate_user_id(user_id)
        self.__name = Validator.validate_name(name)
        self.__email = Validator.validate_email(email)
        
        # Salted Hashing
        self.__salt = SecurityUtils.generate_salt()
        self.__password_hash = SecurityUtils.hash_password(
            password, self.__salt
        )

    @property
    def email((self) -> str:
        return self.__email

    @email.setter
    def email(self, new_email: str):
        self.__email = Validator.validate_email(new_email)"""

    p_snip = tf_code.add_paragraph()
    p_snip.text = snippet_enc
    p_snip.font.name = "Consolas"
    p_snip.font.size = Pt(10.5)
    p_snip.font.color.rgb = TEXT_PRIMARY

    # =========================================================================
    # SLIDE 6: PART B - INHERITANCE & RUNTIME POLYMORPHISM
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide6, prs)
    add_header(slide6, "5. Part B: Inheritance & Runtime Polymorphism")

    # Card 1: Inheritance Structure
    add_card(slide6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=SECONDARY_ACCENT)
    tb_inh = slide6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_inh = tb_inh.text_frame
    tf_inh.word_wrap = True

    p = tf_inh.paragraphs[0]
    p.text = "Inheritance Hierarchy"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SECONDARY_ACCENT
    p.space_after = Pt(12)

    inh_bullets = [
        "Base Class User: Defines abstract core methods (get_privileges(), execute_role_task()).",
        "Derived Administrator: Extends User via super().__init__(). Adds __admin_level, __managed_departments, and lock_user()/unlock_user() methods.",
        "Derived SecurityAnalyst: Extends User via super().__init__(). Adds __clearance_level, __assigned_incidents, and conduct_vulnerability_scan().",
        "Super Function: Reuses parent initialization logic, eliminating duplicate code."
    ]
    for b in inh_bullets:
        p_b = tf_inh.add_paragraph()
        p_b.text = f"•  {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(8)

    # Card 2: Polymorphism Code Snippet
    add_card(slide6, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb_poly = slide6.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_poly = tb_poly.text_frame
    tf_poly.word_wrap = True

    p = tf_poly.paragraphs[0]
    p.text = "Runtime Polymorphism Demo"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_COLOR
    p.space_after = Pt(10)

    snippet_poly = """# List of heterogeneous User objects
users: list[User] = [
    Administrator("ADM-001", "Dr. Sarah", ...),
    SecurityAnalyst("ANA-101", "Alex Mercer", ...)
]

# Polymorphic dispatch at runtime
for u in users:
    # Invokes role-specific get_privileges()
    print(u.get_privileges())

    # Invokes role-specific execute_role_task()
    print(u.execute_role_task())"""

    p_snip = tf_poly.add_paragraph()
    p_snip.text = snippet_poly
    p_snip.font.name = "Consolas"
    p_snip.font.size = Pt(10.5)
    p_snip.font.color.rgb = TEXT_PRIMARY

    # =========================================================================
    # SLIDE 7: PART C - CUSTOM EXCEPTION HANDLING & VALIDATION
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide7, prs)
    add_header(slide7, "6. Part C: Custom Exception Handling & Input Validation")

    # Card 1: Exception Hierarchy
    add_card(slide7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=WARNING_COLOR)
    tb_exc = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_exc = tb_exc.text_frame
    tf_exc.word_wrap = True

    p = tf_exc.paragraphs[0]
    p.text = "Custom Exception Hierarchy"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WARNING_COLOR
    p.space_after = Pt(10)

    exc_tree = """UserManagementException (Base)
├── InvalidEmailException
├── WeakPasswordException
├── InvalidUserIDException
├── AuthenticationFailedException
│   └── AccountLockedException
├── PermissionDeniedException
├── UserAlreadyExistsException
└── UserNotFoundException"""

    p_tree = tf_exc.add_paragraph()
    p_tree.text = exc_tree
    p_tree.font.name = "Consolas"
    p_tree.font.size = Pt(11)
    p_tree.font.color.rgb = TEXT_PRIMARY

    # Card 2: Validation Logic
    add_card(slide7, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb_val = slide7.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_val = tb_val.text_frame
    tf_val.word_wrap = True

    p = tf_val.paragraphs[0]
    p.text = "Validator Routines & Control Flow"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_COLOR
    p.space_after = Pt(12)

    val_bullets = [
        "Email Pattern: Enforces RFC email format using regex (^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$).",
        "User ID Format: Enforces format (e.g. ADM-001, ANA-101) using regex (^[A-Z]{3}-\\d{3,6}$).",
        "Password Complexity: Enforces length >= 8, uppercase, lowercase, digit, and special symbol requirements.",
        "Defensive Control Flow: Standardized try-except-else-finally-raise blocks protect system stability."
    ]
    for b in val_bullets:
        p_b = tf_val.add_paragraph()
        p_b.text = f"•  {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(8)

    # =========================================================================
    # SLIDE 8: PART E - MULTITHREADED ACTIVITY LOGGER
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide8, prs)
    add_header(slide8, "7. Part E: Asynchronous Multithreaded Activity Logger")

    # Card 1: Threading Model
    add_card(slide8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=PRIMARY_ACCENT)
    tb_th = slide8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_th = tb_th.text_frame
    tf_th.word_wrap = True

    p = tf_th.paragraphs[0]
    p.text = "Producer-Consumer Architecture"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_ACCENT
    p.space_after = Pt(12)

    th_bullets = [
        "Non-Blocking Log Dispatch: Main application thread puts log events into queue.Queue without waiting for disk I/O.",
        "Daemon Worker Thread: Background thread (threading.Thread(daemon=True)) continuously reads from queue.",
        "Thread Safety: Thread-safe queue operations prevent race conditions between concurrent user actions.",
        "Clean Shutdown: Provides shutdown() method to flush pending items and join worker thread gracefully."
    ]
    for b in th_bullets:
        p_b = tf_th.add_paragraph()
        p_b.text = f"•  {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(10)

    # Card 2: Code Snippet
    add_card(slide8, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb_th_code = slide8.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_th_code = tb_th_code.text_frame
    tf_th_code.word_wrap = True

    p = tf_th_code.paragraphs[0]
    p.text = "Logger Implementation (logger.py)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_COLOR
    p.space_after = Pt(10)

    snippet_th = """class MultithreadedLogger:
    def __init__(self, log_path):
        self.log_queue = queue.Queue()
        self.worker = threading.Thread(
            target=self._process_logs,
            daemon=True
        )
        self.worker.start()

    def _process_logs(self):
        while self.is_running:
            entry = self.log_queue.get()
            with open(self.log_path, "a") as f:
                f.write(entry + "\\n")
            self.log_queue.task_done()"""

    p_snip = tf_th_code.add_paragraph()
    p_snip.text = snippet_th
    p_snip.font.name = "Consolas"
    p_snip.font.size = Pt(10.5)
    p_snip.font.color.rgb = TEXT_PRIMARY

    # =========================================================================
    # SLIDE 9: PART E - SECURITY CONTROLS & PERSISTENCE
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide9, prs)
    add_header(slide9, "8. Part E: Password Strength Checker, Lockout Policy & Storage")

    # Card 1: Security Controls
    add_card(slide9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=SUCCESS_COLOR)
    tb_sec = slide9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_sec = tb_sec.text_frame
    tf_sec.word_wrap = True

    p = tf_sec.paragraphs[0]
    p.text = "Password Strength & Lockout Policy"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_COLOR
    p.space_after = Pt(12)

    sec_bullets = [
        "Password Strength Evaluator: Calculates score (0-100%) and rating (WEAK, MODERATE, STRONG, VERY STRONG) with actionable feedback.",
        "Login Lockout Policy: Tracks consecutive failed attempts. Locks account (is_locked=True) after 3 failed attempts.",
        "Administrator Authorization: Requires Administrator intervention via unlock_user() to reset failed counter and restore access."
    ]
    for b in sec_bullets:
        p_b = tf_sec.add_paragraph()
        p_b.text = f"•  {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(10)

    # Card 2: Persistence & CSV Export
    add_card(slide9, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2), border_color=WARNING_COLOR)
    tb_st = slide9.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True

    p = tf_st.paragraphs[0]
    p.text = "JSON Persistence & CSV Export"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WARNING_COLOR
    p.space_after = Pt(12)

    st_bullets = [
        "JSON Serialization: Saves polymorphic user objects to data/users.json while preserving subclass type indicators.",
        "State Restoration: Reconstructs exact object instances (Administrator or SecurityAnalyst), restoring salts, hashes, and lock flags.",
        "CSV User Directory: Exports active user roster to data/user_directory_export.csv for external auditing.",
        "Activity Audit Report: Generates summary statistics and formatted text reports (data/activity_summary_report.txt)."
    ]
    for b in st_bullets:
        p_b = tf_st.add_paragraph()
        p_b.text = f"•  {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(10)

    # =========================================================================
    # SLIDE 10: NEW USER REGISTRATION & SELF-SERVICE ONBOARDING
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide10, prs)
    add_header(slide10, "9. New User Registration & Self-Service Onboarding")

    # Card 1: Registration Architecture & Features
    add_card(slide10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=SUCCESS_COLOR)
    tb_reg = slide10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_reg = tb_reg.text_frame
    tf_reg.word_wrap = True

    p = tf_reg.paragraphs[0]
    p.text = "Registration Flow & Features"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_COLOR
    p.space_after = Pt(12)

    reg_bullets = [
        "Main Menu Integration: Direct access via Option 2 ('Register New User Account') from the main application menu.",
        "Inline Registration Prompt: If an unknown User ID is entered during login, the system offers an immediate inline registration prompt.",
        "Role-Based Onboarding: Allows selection of Administrator or Security Analyst role with specific levels/clearances.",
        "Real-Time Defensive Validation: Enforces email RFC validation, User ID regex format, and password strength checks before object instantiation.",
        "Salted PBKDF2 Hashing & Persistence: Automatically salts and hashes credentials and persists updated state to data/users.json."
    ]
    for b in reg_bullets:
        p_b = tf_reg.add_paragraph()
        p_b.text = f"•  {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(8)

    # Card 2: Code Snippet (register_user_flow)
    add_card(slide10, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    tb_reg_code = slide10.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_reg_code = tb_reg_code.text_frame
    tf_reg_code.word_wrap = True

    p = tf_reg_code.paragraphs[0]
    p.text = "Registration Implementation (main.py)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_ACCENT
    p.space_after = Pt(10)

    snippet_reg = """def register_user_flow(self):
    role_type = input("Choice (1=Admin, 2=Analyst): ")
    user_id = input("Enter User ID (e.g. ADM-002): ")
    
    # Check duplicate
    if self.find_user_by_id(user_id):
        raise UserAlreadyExistsException(...)

    # Validate & instantiate polymorphic object
    if role_type == "1":
        new_user = Administrator(user_id, name, email, pass)
    else:
        new_user = SecurityAnalyst(user_id, name, email, pass)

    self.users.append(new_user)
    self.save_state()  # JSON persistence"""

    p_snip = tf_reg_code.add_paragraph()
    p_snip.text = snippet_reg
    p_snip.font.name = "Consolas"
    p_snip.font.size = Pt(10)
    p_snip.font.color.rgb = TEXT_PRIMARY

    # =========================================================================
    # SLIDE 11: SYSTEM VERIFICATION & DEMONSTRATION
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide11, prs)
    add_header(slide11, "10. System Verification, Testing & Deliverables")

    # Card 1: Unit Test Suite
    add_card(slide11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), border_color=SUCCESS_COLOR)
    tb_tst = slide11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_tst = tb_tst.text_frame
    tf_tst.word_wrap = True

    p = tf_tst.paragraphs[0]
    p.text = "Automated Testing (tests/test_system.py)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_COLOR
    p.space_after = Pt(12)

    tst_bullets = [
        "7 Complete Test Cases: Tests encapsulation, properties, dunder methods, inheritance, polymorphism, custom exceptions, account lockout, JSON persistence, and multithreaded logging.",
        "100% Pass Rate: Executed cleanly in 1.458s using unittest runner.",
        "Empirical Proof: Verified zero regressions or unhandled exception leaks."
    ]
    for b in tst_bullets:
        p_b = tf_tst.add_paragraph()
        p_b.text = f"✓  {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(10)

    # Card 2: Deliverables Summary
    add_card(slide11, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2), border_color=PRIMARY_ACCENT)
    tb_del = slide11.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_del = tb_del.text_frame
    tf_del.word_wrap = True

    p = tf_del.paragraphs[0]
    p.text = "Completed Deliverables Checklist"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_ACCENT
    p.space_after = Pt(12)

    del_bullets = [
        "Source Code Package: Modular Python package under secure_system/.",
        "Interactive CLI App: main.py with Login & New User Registration.",
        "Automated E2E Showcase: demo.py demonstrating full system lifecycle.",
        "8-12 Page Technical Report: docs/project_report.md.",
        "UML Class Diagram: docs/uml_class_diagram.md.",
        "PowerPoint Presentation: Secure_User_Management_System_Presentation.pptx."
    ]
    for b in del_bullets:
        p_b = tf_del.add_paragraph()
        p_b.text = f"✓  {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_PRIMARY
        p_b.space_after = Pt(8)

    # Save Presentation
    output_path_docs = "docs/Secure_User_Management_System_Presentation.pptx"
    output_path_root = "Secure_User_Management_System_Presentation.pptx"
    prs.save(output_path_docs)
    prs.save(output_path_root)
    print(f"[+] Presentation successfully created and saved to: {output_path_docs} and {output_path_root}")

if __name__ == "__main__":
    build_presentation()
