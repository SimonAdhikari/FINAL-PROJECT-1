"""
Security Utility Module.

Provides cryptographic hashing (PBKDF2 SHA-256), salt generation,
secure password verification, and strength metrics calculation.
"""

import os
import hashlib
import hmac
import secrets

class SecurityUtils:
    """Cryptographic and security utilities."""

    ITERATIONS = 100_000

    @staticmethod
    def generate_salt() -> str:
        """Generates a secure 16-byte random hex salt."""
        return secrets.token_hex(16)

    @classmethod
    def hash_password(cls, password: str, salt: str) -> str:
        """
        Hashes a password using PBKDF2-HMAC-SHA256 with 100,000 iterations.
        Encapsulates plain-text password into secure hash string.
        """
        hash_bytes = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=salt.encode("utf-8"),
            iterations=cls.ITERATIONS
        )
        return hash_bytes.hex()

    @classmethod
    def verify_password(cls, password: str, stored_hash: str, salt: str) -> bool:
        """
        Verifies password match using constant-time comparison to prevent timing attacks.
        """
        calculated_hash = cls.hash_password(password, salt)
        return hmac.compare_digest(calculated_hash, stored_hash)

    @staticmethod
    def evaluate_password_score(password: str) -> dict:
        """
        Evaluates password strength and returns a score (0-100) and classification.
        Features Part E: Password Strength Checker.
        """
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 25
        else:
            feedback.append("Length under 8 characters (-25%)")

        if len(password) >= 12:
            score += 15

        if any(c.isupper() for c in password):
            score += 15
        else:
            feedback.append("Missing uppercase characters (-15%)")

        if any(c.islower() for c in password):
            score += 15
        else:
            feedback.append("Missing lowercase characters (-15%)")

        if any(c.isdigit() for c in password):
            score += 15
        else:
            feedback.append("Missing digits (-15%)")

        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 15
        else:
            feedback.append("Missing special symbols (-15%)")

        score = min(score, 100)

        if score >= 85:
            rating = "VERY STRONG"
        elif score >= 70:
            rating = "STRONG"
        elif score >= 50:
            rating = "MODERATE"
        else:
            rating = "WEAK"

        return {
            "score": score,
            "rating": rating,
            "feedback": feedback
        }
