from src.mcp.server import Tool
from src.integrations import IdPAdapter, SaaSAdapter, HRISAdapter

class IntegrationTools:
    def __init__(self):
        self.idp = IdPAdapter()
        self.saas = SaaSAdapter()
        self.hris = HRISAdapter()

    def get_tools(self) -> list[Tool]:
        return [
            Tool(
                name="hire_employee",
                description="Hires a new employee into the HRIS and assigns an ID.",
                func=self.hris.hire_employee,
                schema={"name": "str", "email": "str", "department": "str", "role": "str"}
            ),
            Tool(
                name="terminate_employee",
                description="Terminates an employee in HRIS.",
                func=self.hris.terminate_employee,
                schema={"employee_id": "str", "date": "str"}
            ),
            Tool(
                name="grant_ad_group",
                description="Adds a user to an Active Directory group.",
                func=self.idp.add_user_to_group,
                schema={"user_id": "str", "group_name": "str"}
            ),
            Tool(
                name="revoke_ad_group",
                description="Removes a user from an Active Directory group.",
                func=self.idp.remove_user_from_group,
                schema={"user_id": "str", "group_name": "str"}
            ),
            Tool(
                name="grant_gitlab_access",
                description="Grants access to a GitLab project.",
                func=lambda email, project, role: self.saas.update_project_access(email, project, role, "grant"),
                schema={"email": "str", "project": "str", "role": "str"}
            ),
            Tool(
                name="revoke_gitlab_access",
                description="Revokes access to a GitLab project.",
                func=lambda email, project, role: self.saas.update_project_access(email, project, role, "revoke"),
                schema={"email": "str", "project": "str", "role": "str"}
            ),
             Tool(
                name="create_gitlab_user",
                description="Creates a new user in GitLab.",
                func=self.saas.create_user,
                schema={"email": "str", "username": "str"}
            ),
            Tool(
                name="deactivate_user",
                description="Deactivates a user in GitLab/SaaS.",
                func=self.saas.deactivate_user,
                schema={"email": "str"}
            )
        ]
