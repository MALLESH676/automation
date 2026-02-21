import re
from typing import Dict, Tuple

class AIAgent:
    """
    Layer 1: Entry & Intelligence Layer
    Acts as the 'brain' to parse natural language requests.
    """

    def parse_intent(self, text: str) -> str:
        """
        Identifies if the request is a 'Team Transfer', 'Project Change', 'Onboarding', etc.
        """
        text = text.lower()
        if "onboard" in text or "hire" in text or "join" in text:
            return "Onboarding"
        elif "offboard" in text or "terminate" in text or "leaving" in text or "exit" in text:
            return "Offboarding"
        elif "move" in text or "transfer" in text or "change" in text:
            return "Team Transfer" # Can also be "Bulk Transfer" if plural, but keeping simple
        elif "project" in text or "assign" in text:
            return "Project Change"
        elif "leave" in text or "maternity" in text or "sabbatical" in text:
            return "Leave"
        return "Unknown"

    def extract_entities(self, text: str) -> Dict[str, str]:
        """
        Extracts parameters like Person, Target Team, etc.
        """
        entities = {}
        # We work on the raw text for name extraction to preserve case sensitivity if needed,
        # but our pattern will be case-insensitive.
        
        # 1. Name/ID extraction
        # Added 'offboard', 'terminate', 'deactivate' keywords.
        # Support for alphanumeric IDs (e.g. E123)
        # Fixed typo 'praeson' -> 'person'
        name_pattern = r"(?:[Ee]mployee|[Ff]or|[Mm]ove|[Oo]f|[Cc]hange|[Oo]nboard|[Hh]ire|[Oo]ffboard|[Tt]erminate|[Dd]eactivate)(?: the)?(?: person| employee)? (?P<name>[A-Z][a-z]+ [A-Z][a-z]+|[A-Z][a-z]+|[Ee]\d+)"
        
        match_name = re.search(name_pattern, text)
        if match_name:
            entities["person_name"] = match_name.group("name").strip()
        else:
            # Fallback for simpler messages like "move sarah to legal" or "offboard E123"
            # Look for a name or ID at the end of common action phrases
            match_fallback = re.search(r"(?:move|onboard|offboard|terminate|hire) (?P<name>[A-Z][a-z]+|[a-z]+|[Ee]\d+)", text, re.IGNORECASE)
            if match_fallback:
                val = match_fallback.group("name").strip()
                # Title case if it's all lower and not an ID
                if val.islower() and not re.match(r"[Ee]\d+", val):
                    val = val.title()
                entities["person_name"] = val
            
        # 2. Team Extraction (Target & Source)
        text_lower = text.lower()
        # Handle "to [Team]"
        match_target = re.search(r"(?:to|into) (?P<target_team>[\w\s]+?)(?: from| as| under| band|$)", text_lower)
        if match_target:
            entities["target_team"] = match_target.group("target_team").strip()

        # Handle "from [Team]" (Optional)
        match_source = re.search(r"(?:from) (?P<source_team>[\w\s]+?)(?: to| into| as| under| band|$)", text_lower)
        if match_source:
             entities["source_team"] = match_source.group("source_team").strip()
        
        # 3. Role extraction
        match_role = re.search(r"as ([\w\s]+)", text_lower)
        if match_role:
             entities["target_role"] = match_role.group(1).strip().title()

        return entities

    def calculate_confidence(self, text: str, entities: Dict[str, str]) -> float:
        """
        Returns a confidence score between 0.0 and 1.0.
        """
        if entities.get("person_name") and entities.get("target_team"):
            return 0.95
        return 0.2
