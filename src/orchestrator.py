from src.models import TransferRequest, Employee
from src.governance import AuditLogger, NotificationService
from src.mcp.server import MCPServer
from src.mcp.tools import IntegrationTools

class TransferOrchestrator:
    """
    Layer 2: Orchestration Layer (MCP-Based)
    Acts as the AI Controller that selects and executes MCP tools.
    """
    def __init__(self):
        self.audit = AuditLogger()
        self.notifier = NotificationService()
        
        # Initialize MCP Server
        self.mcp = MCPServer()
        self.integration_tools = IntegrationTools()
        
        # Register Tools
        for tool in self.integration_tools.get_tools():
            self.mcp.register_tool(tool)

    def execute_request(self, request: TransferRequest):
        print(f"\n--- Processing Request: {request.intent} ---")
        self.audit.log_event("REQUEST_STARTED", {"intent": request.intent, "file_id": request.request_id})
        
        try:
            if request.intent == "Team Transfer":
                self.handle_transfer(request)
            elif request.intent == "Onboarding":
                self.handle_onboarding(request)
            elif request.intent == "Offboarding":
                self.handle_offboarding(request)
            else:
                print(f"Intent '{request.intent}' not implemented yet.")
                
            request.status = "COMPLETED"
            self.notifier.send_notification("Manager/HR", f"{request.intent} processing COMPLETE.")
            self.audit.log_event("REQUEST_COMPLETED", {"request_id": request.request_id})
            
        except Exception as e:
            print(f"Error executing request: {e}")
            request.status = "FAILED"
            self.audit.log_event("REQUEST_FAILED", {"error": str(e)})

    def handle_transfer(self, request: TransferRequest):
        # 1. Revoke (simplified for MCP demo)
        # In a real agent, the LLM would decide which tools to call.
        # Here we hardcode the logic using the tools.
        
        employee_id = request.employee_id # Assuming ID is resolved
        
        print(">>> Step 1: Revoking Access (via MCP)")
        # For demo, we assume we revoke "Engineering Group"
        self.mcp.call_tool("revoke_ad_group", {"user_id": employee_id, "group_name": "Engineering Group"})
        
        print(">>> Step 2: Granting Access (via MCP)")
        target = request.target_department
        if target:
            self.mcp.call_tool("grant_ad_group", {"user_id": employee_id, "group_name": f"{target} Group"})
            self.mcp.call_tool("grant_gitlab_access", {"email": "sarah@company.com", "project": "Campaign Board", "role": "Editor"})

    def handle_onboarding(self, request: TransferRequest):
        print(">>> Step 1: Hiring in HRIS (via MCP)")
        # Mock data generation from request entities
        name = request.employee_id or "New Hire"
        email = f"{name.replace(' ', '.').lower()}@company.com"
        
        emp_id = self.mcp.call_tool("hire_employee", {
            "name": name, 
            "email": email, 
            "department": request.target_department or "General", 
            "role": request.target_role or "Staff"
        })
        
        print(f">>> Step 2: Provisioning Access for {emp_id}")
        self.mcp.call_tool("create_gitlab_user", {"email": email, "username": name.replace(" ", "")})
        self.mcp.call_tool("grant_ad_group", {"user_id": emp_id, "group_name": "All Employees"})

    def handle_offboarding(self, request: TransferRequest):
        print(">>> Step 1: Terminating in HRIS")
        emp_id = request.employee_id or "E123"
        self.mcp.call_tool("terminate_employee", {"employee_id": emp_id, "date": "Immediate"})
        
        print(">>> Step 2: Revoking All Access")
        # Use simple ID-based email if name-like ID is provided
        email = f"{str(emp_id).lower()}@company.com"
        
        # Check if deactivate_user is available in MCP server
        if "deactivate_user" in self.mcp.tools:
            self.mcp.call_tool("deactivate_user", {"email": email})
        
        self.mcp.call_tool("revoke_ad_group", {"user_id": emp_id, "group_name": "All Employees"})
