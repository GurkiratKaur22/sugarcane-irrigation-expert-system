"""
app.py  -  SIMPLE GUI (Streamlit)
Install once:   pip install streamlit
Run:            streamlit run app.py
Same rules + same engine as the command-line version. Only the screen is new.
"""
import streamlit as st
from rules import RULES, ADVICE_TEXT, SOURCES
from engine import forward_chain, missing_required

st.set_page_config(page_title="Sugarcane Irrigation Advisor", page_icon="🌾")
st.title("🌾 Sugarcane Irrigation Advisor")
st.caption("Rule-based expert system (forward chaining). Fields marked * are required.")

SKIP = "(don't know / skip)"

with st.form("questions"):
    st.subheader("Tell us about your plot")
    age = st.number_input("Crop age in days *", min_value=1, max_value=450, value=None, step=1)
    soil = st.selectbox("Soil type *", ["sandy", "loam", "clay"], index=None, placeholder="Choose...")
    moisture = st.selectbox("Soil moisture *  (dry = crumbles | moderate = slightly moist | wet = sticky/muddy)",
                            ["dry", "moderate", "wet"], index=None, placeholder="Choose...")
    days_irr = st.number_input("Days since last irrigation", min_value=0, max_value=90, value=None, step=1)
    method = st.selectbox("Irrigation method", [SKIP, "flood", "drip"])
    rain48 = st.selectbox("Rain in the last 48 hours", [SKIP, "none", "light", "heavy"])
    forecast = st.selectbox("Chance of rain in the next 48 hours", [SKIP, "low", "high"])
    power = st.number_input("Hours of electricity available today", min_value=0, max_value=24, value=None, step=1)
    harvest = st.number_input("Days left until harvest", min_value=0, max_value=450, value=None, step=1)
    leaf = st.selectbox("Leaf symptoms", [SKIP, "none", "rolling", "yellowing"])
    fert = st.number_input("Days since last fertiliser", min_value=0, max_value=365, value=None, step=1)
    go = st.form_submit_button("Get advice")

if go:
    # Turn the form answers into facts. Skipped answers are left out.
    answers = {
        "crop_age_days": age, "soil_type": soil, "soil_moisture": moisture,
        "days_since_irrigation": days_irr, "irrigation_method": method,
        "rain_last_48h": rain48, "rain_forecast": forecast, "electricity_hours": power,
        "days_to_harvest": harvest, "leaf_symptoms": leaf, "days_since_fertilizer": fert,
    }
    facts = {}
    for key, value in answers.items():
        if value is None or value == SKIP:
            continue
        facts[key] = int(value) if isinstance(value, float) else value

    missing = missing_required(facts)
    if missing:
        st.error("Please fill the required fields: " + ", ".join(missing))
    else:
        final_facts, trace = forward_chain(facts, RULES)

        # ----- ADVICE -----
        st.header("Advisory")
        decision = final_facts.get("decision")
        if decision is None:
            st.warning("Not enough information to decide. Please give more details.")
        else:
            st.success(ADVICE_TEXT[decision])
        if "alert" in final_facts:
            st.error(final_facts["alert"])
        for key in ("method_note", "power_note", "fertigation_note"):
            if key in final_facts:
                st.info(final_facts[key])

        # ----- EXPLANATION TRACE -----
        st.header("Why? (rules that fired, in order)")
        for step in trace:
            icon = "✅" if step["status"] == "FIRED" else "⛔"
            with st.expander(f"{icon} {step['id']}: {step['name']}"):
                st.write(f"**Status:** {step['status']}")
                st.write("**Because:**")
                for line in step["because"]:
                    st.write(f"- {line}")
                st.write(f"**Concluded:** {step['then']}")
                st.write(f"**Source:** {step['source']}  \n{SOURCES.get(step['source'].split(',')[0].strip(), '')}")

        with st.expander("All facts at the end (working memory)"):
            st.json(final_facts)
