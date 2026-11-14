### Health indicators

Each indicator function returns a pair containing its display color and status:

- `("green", "normal")`
- `("orange", "warning")`
- `("red", "critical")`

The app displays the status (`normal`, `warning`, or `critical`) as text and uses
the corresponding color for visual feedback. Status messages are selected from
the same result as the indicator, keeping the message consistent with its
classification.
