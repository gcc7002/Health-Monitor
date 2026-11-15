# Health Monitor

A Streamlit dashboard for astronauts to log health indicators and follow their evolution during a mission. Built for the NASA Space Apps Challenge 2026 (Health Monitoring Software).

> Decision-support prototype. Not a medical device or diagnostic tool.

### dashboard preview

## Features

- Health check-in with automatic timestamp
- Heart rate recorded with its context (rest, activity, post-exercise)
- Activity, well-being and sleep logs
- Color-coded indicator cards
- Timeline with filters and trends
- Synthetic demo data

## Getting started

Requires Python 3.14.2

```bash
git clone https://github.com/gcc7002/Health-Monitor.git
cd Health-Monitor
pip install -r requirements.txt
streamlit run main.py
```

The database starts empty. To load synthetic sample data, run `python storage.py`.

## Limitations

- Status categories are generic references, not NASA protocols or clinical thresholds.
- Radiation values are stored as entered and are not compared against NASA limits.
- Demo data is simulated.

## Future work

- Calendar view
- Wearable and onboard system integration
- Per-astronaut baselines

## References

1. NASA HRP, Five Hazards of Human Spaceflight: https://www.nasa.gov/hrp/hazards
2. NASA HRP, Risks of Human Spaceflight: https://www.nasa.gov/hrp/risks
3. NASA OCHMO, Standards Overview: https://www.nasa.gov/sites/default/files/atoms/files/ochmo_standards_overview_sept_15_2021_francisco.pdf
4. Flynn-Evans E. et al., Humans Are Capable of Achieving Sufficient Sleep in Microgravity (NASA Ames): https://humansystems.arc.nasa.gov/publications/Humans_Sufficient_Sleep_Microgravity.pdf
