import uuid
from src.agent import AIAgent
from src.orchestrator import TransferOrchestrator
from src.models import TransferRequest

def run_verification():
    print("=== Employee Transfer System Verification ===\n")
    
    # Initialize Components
    agent = AIAgent()
    orchestrator = TransferOrchestrator()
    
    # 1. Simulate User Request
    user_input = "Move Sarah to Marketing"
    print(f"Incoming Request: '{user_input}'")
    
    # 2. AI Processing
    intent = agent.parse_intent(user_input)
    entities = agent.extract_entities(user_input)
    confidence = agent.calculate_confidence(user_input, entities)
    
    print(f"AI Analysis: Intent='{intent}', Entities={entities}, Confidence={confidence}")

    if intent == "Team Transfer" and confidence > 0.8:
        # 3. Create Transfer Request
        request = TransferRequest(
            request_id=str(uuid.uuid4()),
            employee_id=entities.get("person_name"),
            target_department=entities.get("target_team"),
            target_role="Specialist", # Default for demo
            requester_id="Manager_Bob",
            intent=intent,
            confidence_score=confidence
        )
        
        # 4. Orchestrate Transfer
        orchestrator.execute_request(request)
        
        print(f"Final Status: {request.status}")
    else:
        print("Request rejected due to low confidence or unclear intent.")

if __name__ == "__main__":
    run_verification()
