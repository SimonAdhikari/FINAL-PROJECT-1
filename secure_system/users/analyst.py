"""
Security Analyst Class Module.

Implements Part B: Derived class SecurityAnalyst inheriting from User.
Demonstrates method overriding, super() usage, and runtime polymorphism.
"""

from secure_system.users.user import User

class SecurityAnalyst(User):
    """
    Derived class representing a Security Analyst responsible for threat detection,
    vulnerability management, and incident response.
    """

    ANALYST_PRIVILEGES = [
        "VULNERABILITY_SCAN",
        "THREAT_LOG_INSPECT",
        "INCIDENT_RESPONSE",
        "SIEM_ALERT_REVIEW",
        "MALWARE_ANALYSIS",
    ]

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        password: str,
        clearance_level: str = "SECRET",
        assigned_incidents: list[str] | None = None
    ):
        # Call superclass constructor (Part B requirement)
        super().__init__(user_id=user_id, name=name, email=email, password=password, role="Security Analyst")
        
        self.__clearance_level = clearance_level.upper()
        self.__assigned_incidents = assigned_incidents or []

    # --- PROPERTIES ---

    @property
    def clearance_level(self) -> str:
        """Getter for security clearance level."""
        return self.__clearance_level

    @clearance_level.setter
    def clearance_level(self, level: str):
        """Setter for clearance level."""
        if level.upper() not in ["UNCLASSIFIED", "CONFIDENTIAL", "SECRET", "TOP_SECRET"]:
            raise ValueError("Clearance level must be UNCLASSIFIED, CONFIDENTIAL, SECRET, or TOP_SECRET.")
        self.__clearance_level = level.upper()

    @property
    def assigned_incidents(self) -> list[str]:
        """Getter for list of assigned incident ticket IDs."""
        return list(self.__assigned_incidents)

    def assign_incident(self, incident_id: str):
        """Assigns an incident to analyst."""
        if incident_id not in self.__assigned_incidents:
            self.__assigned_incidents.append(incident_id)

    def resolve_incident(self, incident_id: str) -> bool:
        """Resolves and removes an incident from assigned list."""
        if incident_id in self.__assigned_incidents:
            self.__assigned_incidents.remove(incident_id)
            return True
        return False

    # --- POLYMORPHIC OVERRIDDEN METHODS (Part B) ---

    def get_privileges(self) -> list[str]:
        """Overrides base User method to return security analyst permission set."""
        privileges = list(self.ANALYST_PRIVILEGES)
        if self.__clearance_level == "TOP_SECRET":
            privileges.append("CLASSIFIED_THREAT_INTEL_ACCESS")
        return privileges

    def execute_role_task(self) -> str:
        """Overrides base User method to execute security scanning task."""
        incidents_str = f"{len(self.__assigned_incidents)} active tickets" if self.__assigned_incidents else "no active tickets"
        return f"[ANALYST TASK] Security Analyst {self.name} (Clearance: {self.__clearance_level}) executed Automated SIEM Threat Analysis and Vulnerability Assessment ({incidents_str})."

    def generate_dashboard_summary(self) -> dict:
        """Overrides base User summary to include analyst-specific metrics."""
        summary = super().generate_dashboard_summary()
        summary.update({
            "Clearance": self.__clearance_level,
            "Active Incidents": len(self.__assigned_incidents),
            "Assigned Tickets": ", ".join(self.__assigned_incidents) if self.__assigned_incidents else "None"
        })
        return summary

    # --- ANALYST SPECIFIC OPERATIONS ---

    def conduct_vulnerability_scan(self, target: str = "Internal Subnet 192.168.1.0/24") -> dict:
        """Simulates a vulnerability scan against target network."""
        return {
            "analyst": self.name,
            "clearance": self.__clearance_level,
            "target": target,
            "status": "COMPLETED",
            "critical_vulnerabilities": 0,
            "high_vulnerabilities": 2,
            "medium_vulnerabilities": 5,
            "recommendation": "Patch OpenSSL service and update firewall rules."
        }

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} | Clearance: {self.__clearance_level} | Incidents: {len(self.__assigned_incidents)}"
