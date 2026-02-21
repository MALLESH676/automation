from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class AccessProfile:
    """Represents a set of permissions for a user."""
    app_name: str  # e.g., "Jira", "Active Directory", "GitHub"
    role: str      # e.g., "Developer", "Viewer", "Admin"
    resource: str  # e.g., "Project A", "Repo X"
    
    def __str__(self):
        return f"{self.app_name} -> {self.role} on {self.resource}"

@dataclass
class Employee:
    """Represents an employee in the organization."""
    id: str
    name: str
    email: str
    department: str
    manager_id: str
    access_rights: List[AccessProfile] = field(default_factory=list)

    def add_access(self, access: AccessProfile):
        self.access_rights.append(access)
    
    def remove_access(self, app_name: str, resource: str):
        self.access_rights = [
            a for a in self.access_rights 
            if not (a.app_name == app_name and a.resource == resource)
        ]

@dataclass
class TransferRequest:
    """Represents a request to transfer an employee."""
    request_id: str
    employee_id: str
    target_department: str  # The new team/dept
    target_role: str        # The new role title
    requester_id: str       # Manager requesting the change
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "PENDING" # PENDING, APPROVED, IN_PROGRESS, COMPLETED, FAILED
    
    # Metadata extracted by NLP
    confidence_score: float = 0.0
    intent: str = "" # "Team Transfer", "Project Change"

