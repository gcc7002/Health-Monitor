### Health indicators

Each indicator function returns a pair containing its display color and status:

- `("green", "normal")`
- `("orange", "warning")`
- `("red", "critical")`

The app displays the status (`normal`, `warning`, or `critical`) as text and uses
the corresponding color for visual feedback. Status messages are selected from
the same result as the indicator, keeping the message consistent with its
classification.

### Health Check

conditions along with the mission

This will take the user to a quick check, where the inputs will be recorded along with the exact time the check is completed. This will allow us to keep our data clean and monitor health conditions throughout the mission.

### Storage

Health checks are stored in health.db

## References

for health measurement

1. NASA Human Research Program — Five Hazards of Human Spaceflight.
   https://www.nasa.gov/hrp/hazards
2. NASA Human Research Program — Risks of Human Spaceflight.
   https://www.nasa.gov/hrp/risks
3. NASA — Risk of Cardiovascular Adaptations.
   https://www.nasa.gov/directorates/esdmd/hhp/risk-of-cardiovascular-adaptations-contributing-to-adverse-mission-performance-and-health-outcomes/
4. NASA OCHMO — Standards Overview (NASA-STD-3001 radiation limits).
   https://www.nasa.gov/sites/default/files/atoms/files/ochmo_standards_overview_sept_15_2021_francisco.pdf
5. NASA OCHMO — Radiation Protection Technical Brief (OCHMO-TB-020).
   https://www.nasa.gov/sites/default/files/atoms/files/radiation_protection_technical_brief_ochmo.pdf

for sleep measurements 6. Flynn-Evans E. et al. — Humans Are Capable of Achieving Sufficient
Sleep in Microgravity (NASA Ames).
https://humansystems.arc.nasa.gov/publications/Humans_Sufficient_Sleep_Microgravity.pdf 7. Barger L.K. et al. (2014). Prevalence of sleep deficiency and use of
hypnotic drugs in astronauts before, during, and after spaceflight.
_The Lancet Neurology_. DOI: 10.1016/S1474-4422(14)70122-X
