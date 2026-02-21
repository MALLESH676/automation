import uuid
from src.agent import AIAgent
from src.orchestrator import TransferOrchestrator
from src.models import TransferRequest

def run_lifecycle_verification():
    print("=== Employee Lifecycle Verification (MCP) ===\n")
    
    agent = AIAgent()
    orchestrator = TransferOrchestrator()
    
    scenarios = [
        "Onboard Jane Doe to Engineering as Developer",
        "Move Sarah to Marketing",
        "Offboard E123" 
    ]
    
    for user_input in scenarios:
        print(f"\n[Test] Input: '{user_input}'")
        
        # 1. AI Processing
        intent = agent.parse_intent(user_input)
        entities = agent.extract_entities(user_input)
        confidence = agent.calculate_confidence(user_input, entities)
        
        print(f"  AI: Intent='{intent}', Entities={entities}")
        
        if confidence > 0.6:
            # 2. execute
            req = TransferRequest(
                request_id=str(uuid.uuid4()),
                employee_id=entities.get("person_name") or "E123", # Fallback for offboarding
                target_department=entities.get("target_team"),
                target_role=entities.get("target_role"),
                requester_id="TestAdmin",
                intent=intent,
                confidence_score=confidence
            )
            
            orchestrator.execute_request(req)
            print(f"  Result: {req.status}")
        else:
            print("  Skipped due to low confidence.")

if __name__ == "__main__":
    run_lifecycle_verification()
