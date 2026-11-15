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

###
