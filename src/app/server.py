from flask import Flask, render_template, request, jsonify
from src.agent import AIAgent
from src.orchestrator import TransferOrchestrator
from src.models import TransferRequest
import uuid
import datetime

app = Flask(__name__)

# Initialize singletons
agent = AIAgent()
orchestrator = TransferOrchestrator()

# Mock database for integration status
INTEGRATIONS = {
    "active_directory": True,
    "gitlab": True,
    "workday": True,
    "slack": False
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/audit-logs')
def audit_logs():
    return render_template('audit_logs.html')

@app.route('/integrations')
def integrations():
    return render_template('integrations.html')

@app.route('/api/integrations', methods=['GET', 'POST'])
def handle_integrations():
    if request.method == 'POST':
        data = request.json
        service = data.get('service')
        status = data.get('status')
        if service in INTEGRATIONS:
            INTEGRATIONS[service] = status
            return jsonify({"status": "success", "service": service, "new_status": status})
        return jsonify({"status": "error", "message": "Service not found"}), 404
    return jsonify(INTEGRATIONS)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # Check if AI processing is "enabled" (proxy for overall system status)
    if not INTEGRATIONS.get('active_directory') and not INTEGRATIONS.get('workday'):
        return jsonify({"response": "I'm sorry, but my core integration nodes (AD/Workday) are currently offline. Please reconnect them in the **Integrations** tab.", "intent": "Error", "entities": {}})

    # 1. AI Processing
    intent = agent.parse_intent(user_message)
    entities = agent.extract_entities(user_message)
    confidence = agent.calculate_confidence(user_message, entities)
    
    response_text = f"I understood you want to perform a **{intent}**."
    if entities:
        response_text += f" Details: {entities}"
    
    # 2. Execute if confidence is high
    if confidence > 0.6:
        req = TransferRequest(
            request_id=str(uuid.uuid4()),
            employee_id=entities.get("person_name"),
            target_department=entities.get("target_team"),
            target_role=entities.get("target_role"),
            requester_id="WebUser",
            intent=intent,
            confidence_score=confidence
        )
        # Check specific integration for the intent
        if intent == "Team Transfer" and not INTEGRATIONS.get('gitlab'):
             response_text += "\n\n**Warning**: GitLab integration is offline. Access changes for GitLab will be skipped."
        
        orchestrator.execute_request(req)
        response_text += f"\n\n**Status**: {req.status}. processing complete."
    else:
        response_text += "\n\nI need more details to proceed."
        
    return jsonify({"response": response_text, "intent": intent, "entities": entities})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    # Read audit log file
    try:
        with open('audit_log.json', 'r') as f:
            import json
            logs = json.load(f)
            
            # Simple server-side filtering (optional, but requested)
            start_date = request.args.get('start')
            end_date = request.args.get('end')
            
            if start_date or end_date:
                # Basic string-based filter for demo
                filtered = []
                for log in logs:
                    log_date = log['timestamp'][:10]
                    if start_date and log_date < start_date: continue
                    if end_date and log_date > end_date: continue
                    filtered.append(log)
                return jsonify(filtered)
                
            return jsonify(logs)
    except Exception as e:
        print(f"Log fetch error: {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

