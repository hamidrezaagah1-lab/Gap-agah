import unittest
from core.framework import TruthFramework
class TestFramework(unittest.TestCase):
    def test_process(self):
        f = TruthFramework()
        self.assertIn("تحلیل", f.process("سلام"))
if __name__ == "__main__":
    unittest.main()
