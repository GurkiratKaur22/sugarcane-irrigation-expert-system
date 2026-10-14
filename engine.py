"""
engine.py  -  THE INFERENCE ENGINE (forward chaining)
------------------------------------------------------
Idea in one line:
    start with known facts -> find rules that match -> fire the best one
    -> it adds a new fact -> repeat until nothing new can happen.
"""
import operator

# What each operator in a rule means
OPS = {
    "==": operator.eq, "!=": operator.ne,
    "<": operator.lt, "<=": operator.le,
    ">": operator.gt, ">=": operator.ge,
    "in": lambda actual, options: actual in options,
}

# Without these 3 facts we cannot give any advice
REQUIRED = ["crop_age_days", "soil_type", "soil_moisture"]


def missing_required(facts):
    """Return the list of required facts the user did not give."""
    return [f for f in REQUIRED if f not in facts]


def resolve(value, facts):
    """If value looks like "$interval_days", replace it with that fact's value."""
    if isinstance(value, str) and value.startswith("$"):
        return facts.get(value[1:])      # None if that fact is not known yet
    return value


def condition_is_true(condition, facts):
    fact, op, value = condition
    if fact not in facts:          # unknown fact -> condition cannot be true
        return False
    value = resolve(value, facts)
    if value is None:              # "$other_fact" is not known yet
        return False
    return OPS[op](facts[fact], value)


def explain_conditions(rule, facts):
    """Turn conditions into readable text, e.g.  crop_age_days <= 35 (actual: 20)"""
    return [f"{f} {op} {v}  (actual: {facts[f]}" + (f", {v} = {resolve(v, facts)})" if str(v).startswith("$") else ")")
            for f, op, v in rule["if"]]


def forward_chain(start_facts, rules):
    """
    Run the rules. Returns (all_facts, trace).
    trace = list of steps, so we can EXPLAIN every decision.
    """
    # Safety check: no advice without the 3 required facts
    if missing_required(start_facts):
        return dict(start_facts), []

    facts = dict(start_facts)      # working memory
    done = set()                   # rules already used (a rule fires only once)
    trace = []

    while True:
        # 1. Which unused rules have ALL conditions true right now?
        matching = [r for r in rules
                    if r["id"] not in done
                    and all(condition_is_true(c, facts) for c in r["if"])]
        if not matching:
            break                  # nothing left to do -> stop

        # 2. CONFLICT RESOLUTION: highest priority wins.
        #    Tie -> rule with more conditions (more specific) wins.
        #    Tie again -> the one written first wins.
        best = max(matching, key=lambda r: (r["priority"], len(r["if"])))
        done.add(best["id"])

        # 3. If a higher-priority rule already decided this fact, BLOCK this rule.
        already_set = [k for k in best["then"] if k in facts]
        step = {"id": best["id"], "name": best["name"], "source": best["source"],
                "because": explain_conditions(best, facts), "then": best["then"]}
        if already_set:
            step["status"] = "BLOCKED (" + ", ".join(already_set) + " already decided by a higher-priority rule)"
        else:
            facts.update(best["then"])   # FIRE: add the new facts
            step["status"] = "FIRED"
        trace.append(step)

    return facts, trace
