"""Deterministic rubric for comparing fixture responses, NOT live model results."""
from pathlib import Path
import json, re
BASE = Path(__file__).resolve().parents[1]

def score(case, response):
    text = response.lower()
    required = case['required']
    coverage = sum(term.lower() in text for term in required) / max(1, len(required))
    numbers = [float(n) for n in re.findall(r'(?<![\w])\d+(?:\.\d+)?', response)]
    # Simple heuristic: derived percentages may be legitimate but need review.
    known = {float(n) for n in case['known_numbers']}
    grounding = 1.0 if all(n in known for n in numbers) else 0.0
    if case['format'] == 'json':
        try:
            payload = json.loads(response)
            format_ok = float(isinstance(payload, dict) and {'summary','recommendation'} <= set(payload))
        except (ValueError, TypeError):
            format_ok = 0.0
    else:
        format_ok = 1.0
    actionability = float(any(x in text for x in ('recommend', 'next step', 'prioritis', 'review', 'investigate', 'compare')))
    return {'coverage':coverage,'grounding_heuristic':grounding,'format':format_ok,'actionability':actionability}

def evaluate(cases, fixtures):
    results = {}
    for variant, replies in fixtures.items():
        totals = []
        for case in cases:
            metrics = score(case, replies[case['id']])
            totals.append(sum(metrics.values())/len(metrics))
        results[variant] = round(sum(totals)/len(totals),3)
    return results

if __name__ == '__main__':
    cases = json.loads((BASE/'data/cases.json').read_text())
    fixtures = json.loads((BASE/'data/fixtures.json').read_text())
    print('Offline fixture rubric scores (not live model evaluations):')
    for name, result in evaluate(cases, fixtures).items():
        print(f'  {name:12s}: {result:.3f}')
