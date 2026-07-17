import unittest
from core.framework import TruthFramework

class TestFramework(unittest.TestCase):
    def test_process_returns_success_dict(self):
        framework = TruthFramework()
        result = framework.process("سلام", mode="general")
        self.assertEqual(result["status"], "success")
        self.assertIn("response", result)
        self.assertEqual(result["mode"], "general")

if __name__ == "__main__":
    unittest.main()
