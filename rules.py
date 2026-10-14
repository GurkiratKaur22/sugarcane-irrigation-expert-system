"""
rules.py  -  THE KNOWLEDGE BASE (v2, numbers now taken from real sources)
-------------------------------------------------------------------------
Every rule = IF (conditions) THEN (conclusions).

A rule has:
  id          : short name, like R01
  name        : what the rule does, in words
  source      : source id (S1, S2...) from SOURCES below, or "ASSUMPTION"
  conditions  : list of (fact, operator, value). ALL must be true.
                value "$xyz" means "use the current value of fact xyz"
  conclusions : dict of new facts the rule adds
  priority    : bigger number = tried first (this is our conflict resolution)

Rules marked ASSUMPTION are team decisions that no source gave us a number
for. Explain them honestly in the report (they are still useful, but
the rubric rewards rules that are grounded in sources).
"""

SOURCES = {
    "S1": "TNAU Agritech Portal, 'Expert System for Sugarcane - Irrigation Management' (Tamil Nadu Agricultural University). "
          "https://agritech.tnau.ac.in/expert_system/sugar/irrigationmanagement.html",
    "S2": "FAO Irrigation and Drainage Paper 56, 'Crop evapotranspiration' (Allen et al., 1998), Table 12 "
          "(sugarcane Kc: 0.4 initial, 1.25 mid, 0.75 late). https://www.fao.org/3/x0490E/x0490e00.htm",
    "S3": "FAO Land & Water, Crop Information: Sugarcane. "
          "https://www.fao.org/land-water/databases-software/crop-information/sugarcane/en/",
    "S4": "IndiaAgroNet, 'Crop Information: Sugarcane' (secondary source: stage days, stop irrigation 15 days before harvest). "
          "https://indiaagronet.com/indiaagronet/crop%20info/sugarcane.htm",
    "S5": "'Reducing sugarcane irrigation demand through planting date' (Embrapa study: irrigation interrupted 30 days before harvest). "
          "https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1136694/1/1019.Reducing-sugarcane-irrigation-demand-through-planting-date-Revista-Brasileira-Lineu.pdf",
    "S6": "MPKV Rahuri (Maharashtra) sugarcane research recommendations 2019-20 (drip at 75% ETc, 3-day interval). "
          "https://mpkv.ac.in/Uploads/Research/9. Sugarcane_20200110053812.pdf",
    "S7": "Study on withholding irrigation before harvest, Omo Kuraz, Ethiopia (50-60 days gave best sugar). "
          "https://ir.amu.edu.et/xmlui/handle/123456789/313",
    "ASSUMPTION": "Team decision (no numeric source found). Justify in report.",
}


def rule(rid, name, source, conditions, conclusions, priority):
    return {"id": rid, "name": name, "source": source,
            "if": conditions, "then": conclusions, "priority": priority}


# Priority layers (big = first):
#  100 stage + soil -> 95 irrigation interval -> 90 water need -> 80 rain
#  -> 70 fallback -> 54-60 final decision -> 35-40 details

RULES = [
    # ===== A: crop stage from crop age (S1: 12-month crop) =====
    rule("R01", "Stage = germination (0-45 days)", "S1",
         [("crop_age_days", "<=", 45)], {"stage": "germination"}, 100),
    rule("R02", "Stage = tillering (46-120 days)", "S1",
         [("crop_age_days", ">", 45), ("crop_age_days", "<=", 120)],
         {"stage": "tillering"}, 100),
    rule("R03", "Stage = grand growth (121-270 days)", "S1",
         [("crop_age_days", ">", 120), ("crop_age_days", "<=", 270)],
         {"stage": "grand_growth"}, 100),
    rule("R04", "Stage = maturity / ripening (over 270 days)", "S1",
         [("crop_age_days", ">", 270)], {"stage": "maturity"}, 100),

    # ===== B: soil texture group (S1 table: coarse / medium / fine) =====
    rule("R05", "Sandy soil = coarse texture (drains fast)", "S1",
         [("soil_type", "==", "sandy")], {"retention": "coarse"}, 100),
    rule("R06", "Loam soil = medium texture", "S1",
         [("soil_type", "==", "loam")], {"retention": "medium"}, 100),
    rule("R07", "Clay soil = fine texture (holds water)", "S1",
         [("soil_type", "==", "clay")], {"retention": "fine"}, 100),

    # ===== C: how many days between irrigations (S1 table, lower end of range) =====
    rule("R08", "Germination + coarse soil: irrigate every 5 days", "S1",
         [("stage", "==", "germination"), ("retention", "==", "coarse")], {"interval_days": 5}, 95),
    rule("R09", "Germination + medium soil: every 6 days", "S1",
         [("stage", "==", "germination"), ("retention", "==", "medium")], {"interval_days": 6}, 95),
    rule("R10", "Germination + fine soil: every 8 days", "S1",
         [("stage", "==", "germination"), ("retention", "==", "fine")], {"interval_days": 8}, 95),
    rule("R11", "Tillering + coarse soil: every 6 days", "S1",
         [("stage", "==", "tillering"), ("retention", "==", "coarse")], {"interval_days": 6}, 95),
    rule("R12", "Tillering + medium soil: every 7 days", "S1",
         [("stage", "==", "tillering"), ("retention", "==", "medium")], {"interval_days": 7}, 95),
    rule("R13", "Tillering + fine soil: every 12 days", "S1",
         [("stage", "==", "tillering"), ("retention", "==", "fine")], {"interval_days": 12}, 95),
    rule("R14", "Grand growth + coarse soil: every 7 days", "S1",
         [("stage", "==", "grand_growth"), ("retention", "==", "coarse")], {"interval_days": 7}, 95),
    rule("R15", "Grand growth + medium soil: every 10 days", "S1",
         [("stage", "==", "grand_growth"), ("retention", "==", "medium")], {"interval_days": 10}, 95),
    rule("R16", "Grand growth + fine soil: every 12 days", "S1",
         [("stage", "==", "grand_growth"), ("retention", "==", "fine")], {"interval_days": 12}, 95),
    rule("R17", "Maturity + coarse soil: every 10 days", "S1",
         [("stage", "==", "maturity"), ("retention", "==", "coarse")], {"interval_days": 10}, 95),
    rule("R18", "Maturity + medium soil: every 12 days", "S1",
         [("stage", "==", "maturity"), ("retention", "==", "medium")], {"interval_days": 12}, 95),
    rule("R19", "Maturity + fine soil: every 15 days", "S1",
         [("stage", "==", "maturity"), ("retention", "==", "fine")], {"interval_days": 15}, 95),

    # ===== D: does the crop need water now? =====
    rule("R20", "Dry soil -> high water need (irrigate before moisture falls too low)", "S1",
         [("soil_moisture", "==", "dry")], {"water_need": "high"}, 90),
    rule("R21", "Wet soil -> no water need (too much water harms roots and buds)", "S1",
         [("soil_moisture", "==", "wet")], {"water_need": "none"}, 90),
    rule("R22", "Moderate moisture and irrigation interval has passed -> medium need", "S1",
         [("soil_moisture", "==", "moderate"), ("days_since_irrigation", ">=", "$interval_days")],
         {"water_need": "medium"}, 90),
    rule("R23", "Moderate moisture, interval not over yet -> no need (fallback)", "S1",
         [("soil_moisture", "==", "moderate")], {"water_need": "none"}, 70),

    # ===== E: rain =====
    rule("R24", "Heavy rain in last 48h -> skip irrigation", "ASSUMPTION",
         [("rain_last_48h", "==", "heavy")], {"rain_effect": "skip"}, 80),
    rule("R25", "High rain forecast -> postpone irrigation", "ASSUMPTION",
         [("rain_forecast", "==", "high")], {"rain_effect": "postpone"}, 80),

    # ===== F: FINAL DECISION (first one that fires wins) =====
    rule("R26", "Near harvest -> STOP irrigation (30 days before harvest)", "S5",
         [("stage", "==", "maturity"), ("days_to_harvest", "<=", 30)],
         {"decision": "STOP_IRRIGATION"}, 60),
    rule("R27", "Dry + leaf rolling + rain forecast -> light irrigation now", "ASSUMPTION",
         [("water_need", "==", "high"), ("leaf_symptoms", "==", "rolling"),
          ("rain_effect", "==", "postpone")],
         {"decision": "IRRIGATE_LIGHT_NOW"}, 59),
    rule("R28", "Recent heavy rain -> no irrigation", "ASSUMPTION",
         [("rain_effect", "==", "skip")], {"decision": "NO_IRRIGATION_RAIN"}, 58),
    rule("R29", "Rain expected soon -> postpone", "ASSUMPTION",
         [("rain_effect", "==", "postpone")], {"decision": "POSTPONE_FOR_RAIN"}, 57),
    rule("R30", "No water need -> no irrigation", "S1",
         [("water_need", "==", "none")], {"decision": "NO_IRRIGATION"}, 56),
    rule("R31", "High water need -> irrigate now", "S1",
         [("water_need", "==", "high")], {"decision": "IRRIGATE_NOW"}, 55),
    rule("R32", "Medium water need -> irrigate within 2 days", "S1",
         [("water_need", "==", "medium")], {"decision": "IRRIGATE_WITHIN_2_DAYS"}, 54),

    # ===== G: details =====
    rule("R33", "Drip: short runs, about every 3 days", "S1, S6",
         [("decision", "in", ["IRRIGATE_NOW", "IRRIGATE_WITHIN_2_DAYS"]),
          ("irrigation_method", "==", "drip")],
         {"method_note": "Drip: run about 2-3 hours and repeat about every 3 days, based on crop water demand."}, 40),
    rule("R34", "Flood: wasteful, suggest furrow", "S1",
         [("decision", "in", ["IRRIGATE_NOW", "IRRIGATE_WITHIN_2_DAYS"]),
          ("irrigation_method", "==", "flood")],
         {"method_note": "Flood irrigation wastes much water; furrow or alternate skip-furrow irrigation saves water."}, 40),
    rule("R35", "Little electricity -> split into two cycles", "ASSUMPTION",
         [("decision", "in", ["IRRIGATE_NOW", "IRRIGATE_WITHIN_2_DAYS", "IRRIGATE_LIGHT_NOW"]),
          ("electricity_hours", "<=", 2)],
         {"power_note": "Power is limited: split irrigation into 2 short cycles in the available hours."}, 35),
    rule("R36", "Dry soil + rolling leaves -> water stress alert", "ASSUMPTION",
         [("soil_moisture", "==", "dry"), ("leaf_symptoms", "==", "rolling")],
         {"alert": "WATER STRESS: crop is suffering, act today."}, 35),
    rule("R37", "Drip + crop 15-210 days + fertiliser 15+ days ago -> fertigation", "S1",
         [("irrigation_method", "==", "drip"), ("crop_age_days", ">=", 15), ("crop_age_days", "<=", 210),
          ("days_since_fertilizer", ">=", 15),
          ("decision", "in", ["IRRIGATE_NOW", "IRRIGATE_WITHIN_2_DAYS"])],
         {"fertigation_note": "Fertigation is due: give N and K fertiliser through the drip (every 15 days, until day 210)."}, 35),
]


# Farmer-friendly sentence for each decision
ADVICE_TEXT = {
    "STOP_IRRIGATION":        "STOP irrigation. Crop is ripening and harvest is close.",
    "IRRIGATE_LIGHT_NOW":     "Irrigate LIGHTLY now (crop is stressed), even though rain is forecast.",
    "NO_IRRIGATION_RAIN":     "Do NOT irrigate. Heavy rain fell recently.",
    "POSTPONE_FOR_RAIN":      "Postpone irrigation. Rain is expected. Check again after 48 hours.",
    "NO_IRRIGATION":          "No irrigation needed today.",
    "IRRIGATE_NOW":           "Irrigate NOW (today).",
    "IRRIGATE_WITHIN_2_DAYS": "Irrigate within the next 2 days.",
}
