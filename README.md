# Sugarcane Irrigation Expert System (Rule-Based, Forward Chaining)

Files
- rules.py        : knowledge base (37 IF-THEN rules) + source list
- engine.py       : inference engine (forward chaining + conflict resolution)
- main.py         : command-line Q&A + advice + explanation   -> python main.py
- app.py          : GUI in the browser (Streamlit)             -> pip install streamlit ; streamlit run app.py
- tests.py        : 14 test cases                              -> python tests.py
- print_rules.py  : rule table + sources for report            -> python print_rules.py
- make_diagram.py : rule dependency diagram                    -> python make_diagram.py
- SOURCES_AND_VALUES.md : where each number came from

CLI needs Python 3.8+ only. GUI needs: pip install streamlit
