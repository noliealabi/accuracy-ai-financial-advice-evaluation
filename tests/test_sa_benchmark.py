import json,unittest
from pathlib import Path
class BenchmarkTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.data=json.loads(Path('data/benchmark_sa.json').read_text(encoding='utf-8'))
 def test_count(self): self.assertEqual(len(self.data),81)
 def test_fields(self):
  req={'id','category','scenario','ai_response','critical_errors','expected_considerations'}
  for x in self.data: self.assertTrue(req.issubset(x)); self.assertEqual(len(x['expected_considerations']),6)
 def test_unique_ids(self): self.assertEqual(len({x['id'] for x in self.data}),81)
