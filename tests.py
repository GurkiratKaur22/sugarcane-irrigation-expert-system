"""
tests.py  -  TEST CASES (D4)
Run:  python tests.py
Each test = inputs + what we EXPECT. We print inputs, fired rules, output, PASS/FAIL.
In 'expected', the value "*" means "this fact must exist (any value)".
"""
from rules import RULES
from engine import forward_chain, missing_required

# Base inputs; each test changes only what it needs
BASE = {"crop_age_days": 150, "soil_type": "loam", "soil_moisture": "dry",
        "days_since_irrigation": 12, "irrigation_method": "flood",
        "rain_last_48h": "none", "rain_forecast": "low",
        "electricity_hours": 8, "leaf_symptoms": "none", "days_since_fertilizer": 60}

TESTS = [
    ("T1 Normal: dry soil, grand growth, loam -> irrigate now",
     {}, {"decision": "IRRIGATE_NOW", "stage": "grand_growth", "interval_days": 10,
          "method_note": "*"}),
    ("T2 Wet soil -> no irrigation",
     {"soil_moisture": "wet"}, {"decision": "NO_IRRIGATION"}),
    ("T3 Dry soil but rain forecast -> postpone",
     {"rain_forecast": "high"}, {"decision": "POSTPONE_FOR_RAIN"}),
    ("T4 CONFLICT: dry + rain forecast + leaves rolling -> light irrigation",
     {"rain_forecast": "high", "leaf_symptoms": "rolling"},
     {"decision": "IRRIGATE_LIGHT_NOW", "alert": "*"}),
    ("T5 EDGE: maturity and 20 days to harvest overrides dry soil -> stop",
     {"crop_age_days": 300, "days_to_harvest": 20}, {"decision": "STOP_IRRIGATION"}),
    ("T6 EDGE: heavy rain last 48h though soil moderate and due -> no irrigation",
     {"soil_moisture": "moderate", "rain_last_48h": "heavy"}, {"decision": "NO_IRRIGATION_RAIN"}),
    ("T7 EDGE: only 2 hours electricity -> split cycles",
     {"soil_type": "sandy", "soil_moisture": "moderate", "days_since_irrigation": 9,
      "electricity_hours": 2}, {"decision": "IRRIGATE_WITHIN_2_DAYS", "power_note": "*"}),
    ("T8a Soil matters: SANDY, grand growth, 8 days -> due (interval 7)",
     {"soil_type": "sandy", "soil_moisture": "moderate", "days_since_irrigation": 8},
     {"decision": "IRRIGATE_WITHIN_2_DAYS", "interval_days": 7}),
    ("T8b Soil matters: CLAY, grand growth, 8 days -> not due (interval 12)",
     {"soil_type": "clay", "soil_moisture": "moderate", "days_since_irrigation": 8},
     {"decision": "NO_IRRIGATION", "interval_days": 12}),
    ("T9 Stage matters: SANDY, germination (age 30), 6 days -> due (interval 5)",
     {"soil_type": "sandy", "soil_moisture": "moderate", "crop_age_days": 30,
      "days_since_irrigation": 6}, {"decision": "IRRIGATE_WITHIN_2_DAYS", "stage": "germination"}),
    ("T10 Stage matters: SANDY, grand growth (age 200), 6 days -> not due (interval 7)",
     {"soil_type": "sandy", "soil_moisture": "moderate", "crop_age_days": 200,
      "days_since_irrigation": 6}, {"decision": "NO_IRRIGATION"}),
    ("T11 Drip + fertiliser due -> drip note and fertigation note",
     {"irrigation_method": "drip"}, {"decision": "IRRIGATE_NOW", "method_note": "*",
                                    "fertigation_note": "*"}),
    ("T12 EDGE: maturity but harvest still 60 days away, soil dry -> keep irrigating",
     {"crop_age_days": 300, "days_to_harvest": 60}, {"decision": "IRRIGATE_NOW", "stage": "maturity"}),
]


def matches(facts, expected):
    for key, value in expected.items():
        if value == "*":
            if key not in facts:
                return False
        elif facts.get(key) != value:
            return False
    return True


def run():
    passed = 0
    for name, changes, expected in TESTS:
        inputs = {**BASE, **changes}
        facts, trace = forward_chain(inputs, RULES)
        fired = [s["id"] for s in trace if s["status"] == "FIRED"]
        blocked = [s["id"] for s in trace if s["status"] != "FIRED"]
        ok = matches(facts, expected)
        passed += ok
        print(f"\n{name}\n  inputs : {changes or '(base inputs)'}\n  fired  : {fired}\n  blocked: {blocked}")
        print(f"  output : decision={facts.get('decision')}")
        print(f"  result : {'PASS' if ok else 'FAIL  expected ' + str(expected)}")

    # Missing required input -> system must refuse politely, not crash
    partial = {"soil_type": "loam", "soil_moisture": "dry"}      # age missing
    facts, trace = forward_chain(partial, RULES)
    ok = missing_required(partial) == ["crop_age_days"] and "decision" not in facts
    passed += ok
    print(f"\nT13 EDGE: missing crop age -> no decision, asks for more info")
    print(f"  missing: {missing_required(partial)}  decision: {facts.get('decision')}")
    print(f"  result : {'PASS' if ok else 'FAIL'}")

    print(f"\n{passed}/{len(TESTS) + 1} tests passed")


if __name__ == "__main__":
    run()
