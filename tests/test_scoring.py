import unittest
from accuracy.scoring import DIMENSIONS, evaluate
class ScoringTests(unittest.TestCase):
 def test_perfect(self): self.assertEqual(evaluate({d:5 for d in DIMENSIONS}).total,40)
 def test_critical_override(self): self.assertTrue(evaluate({d:5 for d in DIMENSIONS},['flag']).classification.startswith('CRITICAL'))
 def test_invalid(self):
  with self.assertRaises(ValueError): evaluate({d:6 for d in DIMENSIONS})
