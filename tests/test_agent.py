import unittest
from src.agent import AIAgent

class TestAIAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AIAgent()

    def test_parse_intent_transfer(self):
        text = "Move Sarah to Marketing"
        self.assertEqual(self.agent.parse_intent(text), "Team Transfer")

    def test_extract_entities_simple(self):
        text = "Move Sarah to Marketing"
        entities = self.agent.extract_entities(text)
        self.assertEqual(entities["person_name"], "Sarah")
        self.assertEqual(entities["target_team"], "Marketing")

    def test_confidence_score_high(self):
        text = "Move Sarah to Marketing"
        entities = {"person_name": "Sarah", "target_team": "Marketing"}
        self.assertEqual(self.agent.calculate_confidence(text, entities), 0.95)

if __name__ == '__main__':
    unittest.main()
