import os
import uuid
import json
from flask import Flask, render_template, request, jsonify
from src.agent import AIAgent
from src.orchestrator import TransferOrchestrator
from src.models import TransferRequest

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

agent = AIAgent()
orchestrator = TransferOrchestrator()

INTEGRATIONS_FILE = "integrations.json"

def load_integration_states():
    if not os.path.exists(INTEGRATIONS_FILE):
        initial_states = {
            "active_directory": False,
            "gitlab": False,
            "workday": False,
            "slack": False
        }
        with open(INTEGRATIONS_FILE, 'w') as f:
            json.dump(initial_states, f)
        return initial_states
    
    try:
        with open(INTEGRATIONS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_integration_states(states):
    with open(INTEGRATIONS_FILE, 'w') as f:
        json.dump(states, f, indent=2)

@app.route('/api/integrations', methods=['GET'])
def get_integrations():
    return jsonify(load_integration_states())

@app.route('/api/integrations', methods=['POST'])
def update_integration():
    data = request.json
    service = data.get('service')
    status = data.get('status')
    
    states = load_integration_states()
    if service in states:
        states[service] = status
        save_integration_states(states)
        return jsonify({"status": "success", "service": service, "new_status": status})
    
    return jsonify({"status": "error", "message": "Service not found"}), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audit-logs')
def audit_logs():
    return render_template('audit_logs.html')

@app.route('/integrations')
def integrations():
    return render_template('integrations.html')

@app.route('/api/logs')
def get_logs():
    log_file = "audit_log.json"
    if not os.path.exists(log_file):
        return jsonify([])
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # 1. AI Analysis
    intent = agent.parse_intent(user_message)
    entities = agent.extract_entities(user_message)
    confidence = agent.calculate_confidence(user_message, entities)
    
    print(f"[API] Intent: {intent}, Entities: {entities}, Confidence: {confidence}")
    
    if intent != "Unknown" and confidence > 0.5:
        # 2. Create Request Object
        req = TransferRequest(
            request_id=str(uuid.uuid4()),
            employee_id=entities.get("person_name"),
            target_department=entities.get("target_team"),
            target_role=entities.get("target_role") or "Specialist",
            requester_id="UI_User",
            intent=intent,
            confidence_score=confidence
        )
        
        # 3. Execute via Orchestrator
        orchestrator.execute_request(req)
        
        response_msg = f"I understood you want to perform a **{intent}**. Details: {entities}\n\n"
        response_msg += f"{intent} processing COMPLETE."
        
        return jsonify({
            "response": response_msg,
            "status": req.status
        })
    else:
        response_msg = f"I understood you want to perform a **{intent}**.\n\n"
        response_msg += "I need more details to proceed. Could you please provide the employee name and target team?"
        return jsonify({
            "response": response_msg,
            "status": "FAILED"
        })

if __name__ == '__main__':
    # Increase recursion limit if needed for complex plans, but shouldn't be necessary here
    app.run(host='127.0.0.1', port=5000, debug=True)
