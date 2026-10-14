"""Prints the rule table + source list (for report D2/D1). Run:  python print_rules.py"""
from rules import RULES, SOURCES

print("| ID | IF | THEN | Source |\n|---|---|---|---|")
for r in RULES:
    cond = " AND ".join(f"{f} {op} {v}" for f, op, v in r["if"])
    then = ", ".join(f"{k} = {v}" for k, v in r["then"].items())
    print(f"| {r['id']} | {cond} | {then} | {r['source']} |")
print(f"\nTotal rules: {len(RULES)}")
grounded = sum(1 for r in RULES if r["source"] != "ASSUMPTION")
print(f"Rules grounded in sources: {grounded}   Team assumptions: {len(RULES) - grounded}")
print("\nSOURCES")
for sid, text in SOURCES.items():
    print(f"{sid}: {text}")
