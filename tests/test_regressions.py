import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.rendering import render_agent_message
from backend.tools.health_tool import workout_split
from backend.tools.productivity_tool import generate_meeting_agenda
from backend.tools.study_tool import grade_needed


class RenderingRegressionTests(unittest.TestCase):
    def test_agent_html_is_escaped(self):
        rendered = render_agent_message(
            {"name": "Agent", "icon": "x"},
            "<script>alert(1)</script>",
            "0.1s",
        )

        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", rendered)


class InputValidationRegressionTests(unittest.TestCase):
    def test_workout_rejects_zero_days(self):
        result = workout_split.invoke({"days_per_week": 0, "goal": "strength"})

        self.assertIn("between 1 and 7", result)

    def test_grade_rejects_weight_above_one_hundred(self):
        result = grade_needed.invoke(
            {
                "current_percent": 80,
                "completed_weight": 120,
                "final_weight": 40,
                "target_percent": 80,
            }
        )

        self.assertIn("between 0 and 100", result)

    def test_meeting_agenda_rejects_empty_topic(self):
        result = generate_meeting_agenda.invoke({"topic": "   "})

        self.assertIn("topic", result.lower())
        self.assertIn("provide", result.lower())


if __name__ == "__main__":
    unittest.main()
