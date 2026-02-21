from typing import List
from src.models import Employee, AccessProfile

class IdPAdapter:
    """Layer 3: Integration Layer - Identity Provider (Mock AD/Okta)"""
    def add_user_to_group(self, user_id: str, group_name: str):
        print(f"[IdP] Adding user {user_id} to group '{group_name}'")

    def remove_user_from_group(self, user_id: str, group_name: str):
        print(f"[IdP] Removing user {user_id} from group '{group_name}'")

class SaaSAdapter:
    """Layer 3: Integration Layer - SaaS Tools (Mock GitLab/GitHub)"""
    def update_project_access(self, user_email: str, project_key: str, role: str, action: str):
        # action: "grant" or "revoke"
        print(f"[SaaS] {action.upper()} access for {user_email} on repository '{project_key}' as {role}")

    def create_user(self, email: str, username: str):
        print(f"[SaaS] Created GitLab user for {email} ({username})")

    def deactivate_user(self, email: str):
        print(f"[SaaS] Deactivated GitLab user {email}")

class HRISAdapter:
    """Layer 3: Integration Layer - HR System (Mock Workday)"""
    def update_employee_record(self, employee_id: str, field: str, value: str):
        print(f"[HRIS] Updating employee {employee_id}: Set {field} = '{value}'")

    def get_employee_details(self, identifier: str) -> Employee:
        # Mock retrieval - identifier can be ID or Name
        # Returning a dummy employee for now to simulate the "Sarah" case
        name = identifier
        return Employee(
            id="E123",
            name=name,
            email=f"{name.lower()}@company.com",
            department="Engineering",
            manager_id="M999",
            access_rights=[
                AccessProfile("Active Directory", "Member", "Engineering Group"),
                AccessProfile("GitLab", "Developer", "Project Alpha"),
                AccessProfile("GitHub", "Contributor", "Repo-Backend")
            ]
        )

    def hire_employee(self, name: str, email: str, department: str, role: str) -> str:
        emp_id = f"E{len(name) * 10}" # Mock ID generation
        print(f"[HRIS] Hired new employee: {name} ({email}) in {department} as {role}. ID assigned: {emp_id}")
        return emp_id

    def terminate_employee(self, employee_id: str, date: str):
        print(f"[HRIS] Terminated employee {employee_id} effective {date}")

    def set_leave_status(self, employee_id: str, status: str, start_date: str, end_date: str):
        print(f"[HRIS] Employee {employee_id} set to {status} from {start_date} to {end_date}")
