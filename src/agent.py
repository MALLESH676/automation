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
        text_lower = text.lower()
        
        # Helper patterns
        name_pattern = r"(?:[Ee]mployee|[Ff]or|[Mm]ove|[Oo]f|[Cc]hange|[Oo]nboard|[Hh]ire)(?: the)?(?: person| employee| praeson)? (?P<name>[A-Z][a-z]+ [A-Z][a-z]+|[A-Z][a-z]+)"
        team_pattern = r"(?:to|into|from) ([\w\s]+) (?:branch|team|project)"
        
        # 1. Name extraction
        match_name = re.search(name_pattern, text)
        if match_name:
            entities["person_name"] = match_name.group("name").strip()
            
        # 2. Team Extraction (Target & Source)
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
