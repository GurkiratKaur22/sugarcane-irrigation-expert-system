# Sources and where each number came from

## What every number in rules.py comes from
| Number in rules | Value | Source |
|---|---|---|
| Stage limits | 0-45, 46-120, 121-270, >270 days | S1 TNAU (12-month crop) |
| Irrigation interval by stage and soil | table below | S1 TNAU |
| Irrigate when | available soil water falls to 50% | S1 TNAU |
| Drip | about every 3 days, 2-3 hour runs | S1 TNAU, S6 MPKV Rahuri |
| Flood | wasteful, furrow saves water | S1 TNAU |
| Fertigation | N and K, every 15 days, from day 15 up to day 210 | S1 TNAU |
| Stop irrigation before harvest | 30 days | S5 (S4 says 15 days, S7 says 50-60 days) |

## TNAU interval table (days between irrigations), used in R08-R19
| Stage | Coarse (sandy) | Medium (loam) | Fine (clay) |
|---|---|---|---|
| Germination (0-45) | 5-6 | 6-7 | 8-10 |
| Tillering (45-120) | 6-7 | 7-10 | 12-15 |
| Grand growth (120-270) | 7 | 10 | 12-15 |
| Ripening (270-360) | 10 | 12-15 | 15-20 |
Rules use the LOWER end of each range (irrigate no later than that day).

## Honest gaps (write these in the report)
- 7 rules are ASSUMPTION: rain rules (R24, R25, R28, R29), light irrigation (R27), electricity limit (R35), leaf-rolling alert (R36). No numeric source found. Explain the logic and mark them as expert-validation items.
- Sources disagree on harvest stop: 15 days (S4), 30 days (S5), 50-60 days (S7). We chose 30. Say why.
- Stage limits differ by source (S4 uses 35/100/270). We chose TNAU, a state agricultural university.
- TNAU table is for Tamil Nadu. Say it is a proxy for North Karnataka and should be checked with KIAAR/GBL or the local agriculture dept.
- Check the use case doc (KJS-AGR-01) yourself for rain and electricity rules and cite the exact section.
- S2 and S3 (FAO) are supporting theory: sugarcane peak water demand at mid season (Kc 1.25). Not used as a rule number.
- Add author and year for S5, S6, S7 by opening the links.
- Open each link yourself once before submitting. Do not cite pages you have not read.
