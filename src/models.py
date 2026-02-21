from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class AccessProfile:
    system: str
    role: str
    group: str

@dataclass
class Employee:
    id: str
    name: str
    email: str
    department: str
    manager_id: str
    access_rights: List[AccessProfile] = field(default_factory=list)

@dataclass
class TransferRequest:
    request_id: str
    employee_id: Optional[str] = None
    target_department: Optional[str] = None
    target_role: Optional[str] = None
    requester_id: Optional[str] = None
    intent: str = "Unknown"
    confidence_score: float = 0.0
    status: str = "PENDING"
