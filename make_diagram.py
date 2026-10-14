"""
make_diagram.py - draws the rule dependency diagram (D2).
Run:  python make_diagram.py
Makes rule_diagram.dot  (+ rule_diagram.png and .svg if Graphviz 'dot' is installed).
No Graphviz? Paste rule_diagram.dot into https://dreampuf.github.io/GraphvizOnline
"""
import shutil, subprocess
from rules import RULES

RED = "#A6192E"          # approximate Somaiya red - replace with the official hex
LIGHT = "#FBEAEC"

# group letter -> (title, first rule, last rule)
GROUPS = {
    "A": ("A. Crop stage", "R01", "R04"),
    "B": ("B. Soil texture", "R05", "R07"),
    "C": ("C. Irrigation interval", "R08", "R19"),
    "D": ("D. Water need", "R20", "R23"),
    "E": ("E. Rain effect", "R24", "R25"),
    "F": ("F. FINAL DECISION", "R26", "R32"),
    "G": ("G. Details & alerts", "R33", "R37"),
}

# (from, to, label)  -> arrows in the diagram
EDGES = [
    ("in_age", "A", "crop_age_days"), ("in_soil", "B", "soil_type"),
    ("A", "C", "stage"), ("B", "C", "retention"),
    ("in_moist", "D", "soil_moisture"), ("in_days", "D", "days_since_irrigation"),
    ("C", "D", "interval_days"),
    ("in_rain", "E", "rain_last_48h /\nrain_forecast"),
    ("A", "F", "stage"), ("in_harvest", "F", "days_to_harvest"),
    ("D", "F", "water_need"), ("E", "F", "rain_effect"),
    ("in_leaf", "F", "leaf_symptoms"),
    ("F", "G", "decision"),
    ("in_method", "G", "irrigation_method"), ("in_power", "G", "electricity_hours"),
    ("in_fert", "G", "days_since_fertilizer"),
    ("G", "out", "notes + alerts"), ("F", "out", "decision"),
]
INPUTS = {"in_age": "crop_age_days *", "in_soil": "soil_type *", "in_moist": "soil_moisture *",
          "in_days": "days_since_irrigation", "in_rain": "rain_last_48h\\nrain_forecast",
          "in_harvest": "days_to_harvest", "in_leaf": "leaf_symptoms",
          "in_method": "irrigation_method", "in_power": "electricity_hours",
          "in_fert": "days_since_fertilizer"}

lines = ["digraph G {", '  rankdir=TB; nodesep=0.35; ranksep=0.55; splines=true;',
         '  node [fontname="DejaVu Sans", fontsize=11]; edge [fontname="DejaVu Sans", fontsize=9, color="#555555"];',
         '  label="Sugarcane irrigation expert system: rule dependency diagram   (* = required input)"; labelloc=t; fontname="DejaVu Sans"; fontsize=14;']
for k, text in INPUTS.items():
    lines.append(f'  {k} [label="{text}", shape=box, style="rounded,filled", fillcolor="#EEEEEE", color="#999999"];')
for g, (title, first, last) in GROUPS.items():
    ids = [r["id"] for r in RULES if first <= r["id"] <= last]
    label = f"{title}\\n{ids[0]}-{ids[-1]}  ({len(ids)} rules)"
    fill = RED if g == "F" else LIGHT
    font = "white" if g == "F" else "black"
    lines.append(f'  {g} [label="{label}", shape=box, style="filled", fillcolor="{fill}", fontcolor="{font}", color="{RED}", penwidth=2];')
lines.append(f'  out [label="ADVISORY\\n+ explanation trace\\n(which rules fired and why)", shape=box, style="rounded,filled", fillcolor="#DFF0D8", color="#3C763D"];')
for a, b, lab in EDGES:
    lines.append(f'  {a} -> {b} [label="{lab}"];')
lines.append("  {rank=same; in_age; in_soil; in_moist; in_days; in_rain}")
lines.append("}")
open("rule_diagram.dot", "w").write("\n".join(lines))
print("wrote rule_diagram.dot")

if shutil.which("dot"):
    subprocess.run(["dot", "-Tpng", "-Gdpi=200", "rule_diagram.dot", "-o", "rule_diagram.png"], check=True)
    subprocess.run(["dot", "-Tsvg", "rule_diagram.dot", "-o", "rule_diagram.svg"], check=True)
    print("wrote rule_diagram.png and rule_diagram.svg")
else:
    print("Graphviz not installed: paste rule_diagram.dot into https://dreampuf.github.io/GraphvizOnline")
