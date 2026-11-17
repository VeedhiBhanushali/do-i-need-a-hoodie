# Do I Need a Hoodie?

## Authors

- Veedhi Bhanushali (`@VeedhiBhanushali`)
- Joseph "Joey" Lee (`@JLTheEarthworm`)

## Project Description

This Python app will help users decide what layer to bring when they go out. Users will choose a city, the date and hours they plan to be outside, and how easily they get cold. The app will download hourly weather forecasts from Open-Meteo and save the data so users can open it again later. It will look at the lowest feels-like temperature, the temperature change, wind, and chance of precipitation during the outing to give a simple clothing suggestion. A graph will show the temperature throughout the outing so users can see why the app recommends a hoodie, a warmer jacket, or no extra layer.

## Project Outline and Plan

### Interface Plan

I plan to use Tkinter to build two windows. The main window will let users plan an outing and download or open weather data. The results window will show the recommendation, a short explanation, a weather summary, and a graph.

The first version will use a small city list with stored coordinates, including San Jose, San Francisco, Los Angeles, and New York. Users will choose an outing within the next seven days, using the selected city's local time. For the first version, the start and end times must be on the same day.

Planned interactive widgets:

1. City dropdown.
2. Outing date dropdown.
3. Start hour dropdown.
4. End hour dropdown.
5. Cold tolerance dropdown: gets cold easily, average, or usually warm.
6. Celsius/Fahrenheit dropdown.
7. Get forecast button.
8. Open saved forecast button.
9. Save forecast button.
10. Show recommendation button, which opens the results window.
11. Show graph button in the results window.
12. Export graph button.
13. Close results button.

The app will show a message for missing choices, invalid time ranges, unavailable forecasts, or failed downloads. Opening an old forecast will show its download time so users know it may be outdated.

### Data Collection and Storage Plan - Veedhi's Role

I will use `requests` to download hourly temperature, apparent temperature (feels-like temperature), precipitation probability, and wind speed from the Open-Meteo Forecast API. Requests will use the city's coordinates and local time zone. The program will check that the response contains the requested hours and variables before using it.

The original response will be saved as JSON, and the hourly records will be organized into CSV files in a `data/` folder. The records will include city, coordinates, local date and time, temperature in Celsius, feels-like temperature in Celsius, precipitation probability in percent, and wind speed in km/h. The JSON will also keep the download time, time zone, source, and units. Filenames will identify the city and download time, and users will be able to reopen a saved forecast.

Data source: https://open-meteo.com/en/docs

The app and README will credit Open-Meteo and its required data providers. Forecasts will be labeled as predictions. Missing values will not be replaced with zero, and an incomplete feels-like series will not produce a confident clothing recommendation.

### Data Analysis and Visualization Plan - Joey's Role

### Data Analysis and Visualization Plan - Joey's Role

For my part of the project, I'll be working on analyzing the weather data and displaying the results to the user. I'll use pandas to look at the weather conditions during the selected outing hours and calculate the lowest and average feels-like temperatures, the temperature change throughout the outing, the highest wind speed, and the highest hourly chance of precipitation.

I'll also be responsible for creating the clothing recommendation system. The recommendations will mainly depend on the lowest feels-like temperature during the outing:

- Below 10°C: Recommend bringing a warmer jacket.
- Between 10°C and 18°C (not including 18°C): Recommend bringing a hoodie.
- 18°C or higher: An extra layer might not be necessary.

I'll also account for the user's cold tolerance. If someone gets cold easily, I'll increase the temperature thresholds by 2°C. If someone usually feels warm, I'll decrease them by 2°C. I'll include an additional suggestion to bring an umbrella or rain-resistant clothing if there's a high chance of precipitation.

For the visualization part, I plan to use Matplotlib to create a graph showing the actual temperature and feels-like temperature throughout the outing. The graph will include the selected city, date, labeled axes, a legend, and a reference line showing the temperature threshold for recommending a hoodie.

I'll also make it possible for users to switch between Celsius and Fahrenheit and save the graph as a PNG image. The temperature values and thresholds will change based on the selected unit, but the clothing recommendation itself will stay the same.

### Planned Steps

1. Establish the shared project structure and contribution workflow.
2. Download a sample forecast and organize the saved files.
3. Build the main Tkinter window.
4. Write the weather summaries and recommendation rules.
5. Build the results window and temperature graph.
6. Add file loading, saving, and graph export.
7. Test different cold tolerances, dates, units, missing values, and failed downloads.
8. Finish the README instructions and prepare a short demonstration.

Our current work split and next steps are in
[`docs/team_plan.md`](docs/team_plan.md).

## Planned Tools

- Python
- Tkinter
- requests
- pandas
- Matplotlib

## Project Status

The team is confirmed and we are starting the first working version. The first
step is reading hourly weather data from Open-Meteo and turning it into a format
the rest of the app can use.

## Possible Future Improvements

- Add city search instead of a fixed city list.
- Support outings that continue past midnight.
- Let users adjust their own temperature cutoffs.
- Compare two destinations for a day trip.

## License

The project code is licensed under the MIT License. Weather data remains subject to its source licenses and attribution requirements.
