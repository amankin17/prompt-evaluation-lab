import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from evaluate import score, evaluate

class RubricTests(unittest.TestCase):
    def test_complete_json(self):
        c={'required':['revenue'],'format':'json','known_numbers':[10]}
        result=score(c,'{"summary":"revenue 10", "recommendation":"Review"}')
        self.assertEqual(result,{'coverage':1,'grounding_heuristic':1,'format':1,'actionability':1})
    def test_unsupported_number_flagged(self):
        c={'required':['revenue'],'format':'text','known_numbers':[10]}
        self.assertEqual(score(c,'revenue 999')['grounding_heuristic'],0)
    def test_json_rejection(self):
        c={'required':[],'format':'json','known_numbers':[]}
        self.assertEqual(score(c,'not json')['format'],0)
if __name__=='__main__': unittest.main()
