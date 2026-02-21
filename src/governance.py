import json
from datetime import datetime
import os

class AuditLogger:
    """Layer 4: Governance & Observability - Audit Log"""
    
    def __init__(self, log_file="audit_log.json"):
        self.log_file = log_file
        # Initialize file if not exists
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def log_event(self, event_type: str, details: dict):
        """
        Logs an event to the audit trail.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        }
        
        # Read existing logs
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
            
        logs.append(entry)
        
        # Write back
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)
            
        print(f"[Audit] Event logged: {event_type}")

class NotificationService:
    """Layer 4: Governance & Observability - Notifications"""
    
    def send_notification(self, recipient: str, message: str):
        """
        Mock notification sender (Email/Slack).
        """
        print(f"\n[Notification] To: {recipient}")
        print(f"[Notification] Message: {message}\n")
