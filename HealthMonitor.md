# Health Monitor

## 1. Project overview

Health Monitor is a health-tracking prototype for space missions. It is intended to help crew members record health indicators and events, review their history throughout a mission, and find useful information to decide when to monitor a change or seek guidance.

The system is a tracking tool. It does not replace clinical assessment, mission protocols, or communication with the medical team.

## 2. Challenge context

The NASA Space Apps challenge considers risks associated with five hazards of spaceflight:

1. Space radiation.
2. Isolation and confinement.
3. Distance from Earth.
4. Gravity fields and altered gravity.
5. Hostile and closed environments.

NASA links these hazards to a range of health risks, including cardiovascular changes, bone and muscle loss, sleep changes, inadequate nutrition, and behavioral health impacts.

Distance from Earth can also increase communication delays. During a Mars mission, one-way communication delay can reach about 20 minutes, depending on the planets' relative positions. This reinforces the value of an interface that helps astronauts record and understand information without relying on immediate communication.

## 3. Indicators and events considered

### 3.1 Health check-in

- Heart rate (bpm), interpreted in the context of the measurement.
- Oxygen saturation (SpO₂).
- Systolic and diastolic blood pressure.
- Body temperature.
- Optional symptoms and notes.
- Measurement context and source.
- Radiation exposure when a value and its source are available.

### 3.2 Activity

- Activity type, description, and duration.
- Optional perceived intensity.
- Average and maximum heart rate, when available.
- Estimated calories burned, distinguished from calories consumed.
- Source of measured or estimated values.

### 3.3 Well-being

- Self-reported mood on a scale from 1 to 5.
- Stress and feelings of isolation as separate, optional responses.
- Optional free-text note.
- Perceived sleep quality, separate from sleep duration.

### 3.4 Sleep

- Sleep period start and end times.
- Duration calculated from the recorded interval.
- Optional perceived quality, interruptions, and notes.

## 4. Evidence and reference metrics

The values below provide context for research and prototype design. They should not automatically be presented as a diagnosis, an individual limit, or an operational protocol. Before implementing alerts, confirm the primary source, current standard version, applicable population, units, and measurement period.

### Sleep

- NASA schedules sleep opportunities of approximately 8.5 hours in some operational contexts.
- Cited studies report different average sleep durations across crews and missions; values vary by population, mission, and measurement method.
- A general recommendation of at least seven hours is not, by itself, a clinical threshold specific to each astronaut.
- In the prototype, sleep duration should be presented as a recorded value and trend. The seven-hour reference and the 8.5-hour scheduled opportunity should be identified as distinct references, not combined into one universal range.

### Exercise and cardiovascular health

- Exercise is used during missions as a countermeasure to help reduce losses in bone density, muscle strength, and cardiovascular capacity.
- Microgravity can alter circulation and the function of the heart and blood vessels.
- Heart-rate readings should include context, such as rest or activity. Do not automatically interpret readings during or after exercise using the same rules as readings taken at rest.

### Mental health and isolation

- Isolation, confinement, distance from Earth, and other stressors can affect psychological well-being.
- Mood, stress, and feelings of isolation are distinct self-reports; the scale and meaning of responses should be explained to users.
- Sleep, lighting, and physical activity are relevant factors in isolated mission environments.

### Radiation

- Radiation exposure should be treated as mission data, separate from signals describing the body's state at a particular moment.
- Measurements may come from personal dosimeters or area monitoring; record the source, unit, and reference period.
- The values of 600 mSv for a career limit, 250 mSv per solar particle event, and about 1.3 mSv/day for galactic cosmic rays in free space are mentioned in NASA technical documents in specific contexts. Confirm the current edition and context of each value before using it in the application.
- In particular, an environmental daily rate must not be presented as an individual daily limit. Cumulative dose and event exposure are not interchangeable.

## 5. Current prototype status

### Already structured

- Streamlit dashboard with indicators and the latest records.
- Forms for health check-ins, activity, well-being, and sleep.
- Local SQLite persistence, with tables for the different record types.
- Timestamp or time interval recorded according to the event type.
- Chronological timeline with filters, event-type summaries, and trends.
- Shared modules for storage, indicator rules, and interface components.

### In progress or to complete

- Calendar is still marked as WIP.
- Consolidate the most recent record time and measurement context on the dashboard.
- Link each indicator to relevant spaceflight hazards and risks with short “why measure this?” explanations.
- Make it clear that activity and calorie data may be estimates and distinguish their sources.
- Define how to display sleep over time, including periods that cross midnight.
- Review status rules: current ranges are generic and need appropriate sourcing and validation before they can guide medical decisions.

## 6. Suggested priorities

| Priority | Item | Goal | Note |
|---|---|---|---|
| 1 | Heart-rate context | Distinguish readings at rest, after exercise, and during activity | Avoid classifying readings without context |
| 2 | “Why measure this?” explanations | Connect each indicator to mission-related risks | Keep the text brief, informative, and sourced |
| 3 | Well-being | Track mood from 1 to 5, stress, and isolation separately | Make clear these are self-reports |
| 4 | Sleep | Show duration and trends, distinguishing general references from scheduled opportunities | Do not treat 7 h and 8.5 h as equivalent |
| 5 | Physical activity | Summarize activity duration and frequency over time | Duration can be derived from recorded start and end times |
| 6 | Radiation | Show exposure, period, source, and cumulative dose if appropriate | Do not implement alerts until limits and context are validated |
| 7 | Calendar | Allow users to review records by mission day | May remain WIP if the timeline meets current demo needs |
| 8 | Guidance and escalation | Explain next steps and when to follow a protocol or contact the medical team | Use approved sources/protocols; do not generate diagnoses |

## 7. Data and interface best practices

- Show each value with its unit, timestamp, and context.
- Identify whether data was measured by a sensor, reported by the user, or estimated.
- Treat unrecorded fields as unavailable, never as zero.
- Do not combine different indicators into a single “health” score.
- Keep bodily signals, self-reports, activity events, and exposure data distinct.
- Display trends only when enough records exist; do not invent values between measurements.
- Use clear language and an accessible tablet-sized layout, with large controls and few steps per form.
- Distinguish educational information from clinical guidance; show medical alerts only when supported by validated evidence and an appropriate protocol.
- Use fictional data for demonstrations and protect the local database, which contains health information.

## 8. References

### Spaceflight hazards and risks

1. NASA Human Research Program — Five Hazards of Human Spaceflight.  
   https://www.nasa.gov/hrp/hazards
2. NASA Human Research Program — Risks of Human Spaceflight.  
   https://www.nasa.gov/hrp/risks
3. Review article on human health risks in spaceflight.  
   https://pmc.ncbi.nlm.nih.gov/articles/PMC7645687/
4. NASA — Risk of Cardiovascular Adaptations.  
   https://www.nasa.gov/directorates/esdmd/hhp/risk-of-cardiovascular-adaptations-contributing-to-adverse-mission-performance-and-health-outcomes/

### Sleep, isolation, and behavioral health

5. Flynn-Evans E. et al. — Humans Are Capable of Achieving Sufficient Sleep in Microgravity (NASA Ames).  
   https://humansystems.arc.nasa.gov/publications/Humans_Sufficient_Sleep_Microgravity.pdf
6. Barger L.K. et al. (2014). Prevalence of sleep deficiency and use of hypnotic drugs in astronauts before, during, and after spaceflight. *The Lancet Neurology*. DOI: 10.1016/S1474-4422(14)70122-X
7. NASA — Health and performance risks of isolation and distance.  
   https://www.nasa.gov/?p=936108
8. Space.com — Spaceflight risks and communication delay context.  
   https://www.space.com/42918-big-space-risks-mars-astronauts-videos.html
9. Deccan Herald — Report on astronaut sleep. Use as secondary context; prefer NASA studies for technical claims.  
   https://www.deccanherald.com/archives/astronauts-suffer-serious-sleep-deprivation-2203740

### Standards and radiation protection

10. NASA OCHMO — Standards Overview.  
    https://www.nasa.gov/sites/default/files/atoms/files/ochmo_standards_overview_sept_15_2021_francisco.pdf
11. NASA OCHMO — Radiation Protection Technical Brief (OCHMO-TB-020).  
    https://www.nasa.gov/wp-content/uploads/2023/03/radiation-protection-technical-brief-ochmo.pdf
