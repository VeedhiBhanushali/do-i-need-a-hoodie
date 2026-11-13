# Team Plan

## Project goal

Build a small Tkinter application that retrieves an Open-Meteo forecast for a
selected city and outing window, saves the forecast locally, and explains what
outer layer may be comfortable. The recommendation is a transparent comfort
rule, not a safety or medical claim.

## Responsibilities

### Veedhi Bhanushali

- Maintain the Open-Meteo request and response-validation code.
- Define the forecast data model and JSON/CSV storage format.
- Build the main Tkinter inputs and connect the interface to the data layer.
- Keep setup and data-source documentation current.

### Joseph "Joey" Lee

- Implement outing-window summaries and clothing-recommendation rules.
- Build the results view and Matplotlib temperature visualization.
- Add tests for analysis edge cases, cold-tolerance adjustments, and units.
- Review the interface flow and help prepare the final demonstration.

Both partners will review changes that cross these boundaries. Tasks may move
when one part blocks another, but the commit or pull-request description should
say who completed and reviewed the work.

## Working agreement

1. Make focused commits with a short explanation of what changed.
2. Use a branch and pull request for each feature-sized change.
3. Add or update tests with behavior changes.
4. Do not commit API secrets, virtual environments, or generated forecast data.
5. Coordinate through email and GitHub so project decisions stay easy to find.

## Milestones

### Milestone 1 — foundation

- [x] Agree on the project and partner roles.
- [ ] Add the Python package structure and forecast data model.
- [ ] Add initial validation tests.

### Milestone 2 — data and analysis

- [ ] Fetch and validate Open-Meteo hourly forecasts.
- [ ] Save and reopen JSON/CSV forecast files.
- [ ] Summarize an outing window and produce a recommendation.

### Milestone 3 — interface and visualization

- [ ] Build the main Tkinter input flow.
- [ ] Build the results window and chart.
- [ ] Support Celsius/Fahrenheit display and PNG export.

### Milestone 4 — integration and demonstration

- [ ] Test success, invalid-input, missing-data, and failed-request paths.
- [ ] Complete installation and usage instructions.
- [ ] Prepare sample data and a short demonstration checklist.

## First handoff for Joey

Once the foundation pull request is available, Joey can start the analysis work
on a branch named `joey/analysis-rules`. The first deliverable should take a
validated list of hourly records plus a start/end time and return:

- minimum and average apparent temperature;
- first-to-last temperature change;
- maximum wind speed;
- maximum hourly precipitation probability; and
- a recommendation label plus a short human-readable explanation.

The initial thresholds and cold-tolerance adjustments are described in the main
README. Tests should cover each recommendation band, both tolerance offsets,
rain guidance, and an incomplete apparent-temperature series.
