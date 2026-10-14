"""
main.py  -  THE USER INTERFACE (command line)
Run:  python main.py
It asks questions, runs the engine, prints advice + explanation.
"""
from rules import RULES, ADVICE_TEXT
from engine import forward_chain, missing_required


# ---------- small helpers to ask questions safely ----------

def ask_number(fact, question, low, high, required=False):
    """Ask for a whole number. Enter = skip (only if not required)."""
    while True:
        text = input(f"{question}\n   > ").strip()
        if text == "" and not required:
            return None
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
        print(f"   Please type a whole number from {low} to {high}.", "" if required else "(or press Enter to skip)")


def ask_choice(fact, question, options, required=False):
    """Show numbered options. Accept the number or the word. Enter = skip."""
    menu = "   ".join(f"{i}) {o}" for i, o in enumerate(options, 1))
    while True:
        text = input(f"{question}\n   {menu}\n   > ").strip().lower()
        if text == "" and not required:
            return None
        if text in options:
            return text
        if text.isdigit() and 1 <= int(text) <= len(options):
            return options[int(text) - 1]
        print("   Please pick one of the options.", "" if required else "(or press Enter to skip)")


def collect_facts():
    """Ask all questions. Returns a dict of facts (skipped ones are left out)."""
    print("\nAnswer the questions. Press Enter to skip an optional question.\n")
    answers = {
        "crop_age_days": ask_number("crop_age_days", "1. Crop age in days (required)", 1, 450, required=True),
        "soil_type": ask_choice("soil_type", "2. Soil type (required)", ["sandy", "loam", "clay"], required=True),
        "soil_moisture": ask_choice("soil_moisture",
            "3. Soil moisture (required). dry = crumbles, no moisture | moderate = slightly moist | wet = sticky/muddy",
            ["dry", "moderate", "wet"], required=True),
        "days_since_irrigation": ask_number("days_since_irrigation", "4. Days since last irrigation", 0, 90),
        "irrigation_method": ask_choice("irrigation_method", "5. Irrigation method", ["flood", "drip"]),
        "rain_last_48h": ask_choice("rain_last_48h", "6. Rain in the last 48 hours", ["none", "light", "heavy"]),
        "rain_forecast": ask_choice("rain_forecast", "7. Chance of rain in the next 48 hours", ["low", "high"]),
        "electricity_hours": ask_number("electricity_hours", "8. Hours of electricity available today", 0, 24),
        "days_to_harvest": ask_number("days_to_harvest", "9. Days left until harvest", 0, 450),
        "leaf_symptoms": ask_choice("leaf_symptoms", "10. Leaf symptoms", ["none", "rolling", "yellowing"]),
        "days_since_fertilizer": ask_number("days_since_fertilizer", "11. Days since last fertiliser", 0, 365),
    }
    return {k: v for k, v in answers.items() if v is not None}


# ---------- printing the result ----------

def print_advice(facts):
    print("\n" + "=" * 60)
    print("ADVISORY")
    print("=" * 60)
    decision = facts.get("decision")
    if decision is None:
        print("Not enough information to decide. Please give more details or ask the field assistant.")
        return
    print(ADVICE_TEXT[decision])
    for key in ("method_note", "power_note", "fertigation_note", "alert"):
        if key in facts:
            print("-", facts[key])


def print_trace(trace):
    print("\n" + "=" * 60)
    print("WHY? (which rules fired)")
    print("=" * 60)
    for step in trace:
        print(f"\n[{step['id']}] {step['name']}   -> {step['status']}")
        for line in step["because"]:
            print(f"     because {line}")
        print(f"     concluded: {step['then']}")
        print(f"     source: {step['source']}")


def main():
    print("SUGARCANE IRRIGATION ADVISORY (rule-based expert system)")
    while True:
        facts = collect_facts()
        final_facts, trace = forward_chain(facts, RULES)
        print_advice(final_facts)
        print_trace(trace)
        again = input("\nCheck another plot? (y/n) > ").strip().lower()
        if again != "y":
            print("Thank you!")
            break


if __name__ == "__main__":
    main()
