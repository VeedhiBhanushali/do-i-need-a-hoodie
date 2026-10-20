# Do I Need a Hoodie?

## Authors

Veedhi Bhanushali

Partner: not assigned yet. I prepared this proposal individually. The team arrangement and division of work still need to be confirmed with the instructor.

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

### Data Collection and Storage Plan - Author #1 Role

Prepared by Veedhi Bhanushali while the partner assignment is pending.

I will use `requests` to download hourly temperature, apparent temperature (feels-like temperature), precipitation probability, and wind speed from the Open-Meteo Forecast API. Requests will use the city's coordinates and local time zone. The program will check that the response contains the requested hours and variables before using it.

The original response will be saved as JSON, and the hourly records will be organized into CSV files in a `data/` folder. The records will include city, coordinates, local date and time, temperature in Celsius, feels-like temperature in Celsius, precipitation probability in percent, and wind speed in km/h. The JSON will also keep the download time, time zone, source, and units. Filenames will identify the city and download time, and users will be able to reopen a saved forecast.

Data source: https://open-meteo.com/en/docs

The app and README will credit Open-Meteo and its required data providers. Forecasts will be labeled as predictions. Missing values will not be replaced with zero, and an incomplete feels-like series will not produce a confident clothing recommendation.

### Data Analysis and Visualization Plan - Author #2 Role

Proposed by Veedhi Bhanushali. A second author has not been assigned, so this section is not being claimed as another person's contribution.

I will use pandas to select the hours during the outing and calculate the lowest and average feels-like temperatures, the change from the first hour to the last hour, the highest wind speed, and the highest hourly precipitation probability. The highest hourly probability will be labeled clearly; it is not the probability of precipitation over the entire outing.

The first recommendation rules will use the lowest feels-like temperature in the outing:

- Below 10 degrees Celsius: bring a warmer jacket.
- From 10 to below 18 degrees Celsius: bring a hoodie.
- At least 18 degrees Celsius: an extra layer may not be needed.

For someone who gets cold easily, the temperature cutoffs will increase by 2 degrees Celsius. For someone who usually feels warm, they will decrease by 2 degrees Celsius. A high precipitation probability will add a separate suggestion to bring an umbrella or a rain-resistant layer. Wind will appear in the explanation, but I will not apply another wind-chill adjustment because apparent temperature already accounts for wind and other weather conditions. These are adjustable comfort rules rather than a guarantee of what everyone should wear.

Matplotlib will show actual and feels-like temperature across the selected hours. The graph will include the city and outing date, labeled axes with units, a legend, and a horizontal line for the user's hoodie cutoff. Users will be able to save the graph as a PNG. Changing the displayed temperature units will convert the values and cutoff together without changing the recommendation.

### Planned Steps

1. Confirm the partner arrangement with the instructor.
2. Download a sample forecast and organize the saved files.
3. Build the main Tkinter window.
4. Write the weather summaries and recommendation rules.
5. Build the results window and temperature graph.
6. Add file loading, saving, and graph export.
7. Test different cold tolerances, dates, units, missing values, and failed downloads.
8. Finish the README instructions and prepare a short demonstration.

## Planned Tools

- Python
- Tkinter
- requests
- pandas
- Matplotlib

## Project Status

This repository currently contains the proposal. The app has not been implemented yet. Installation and run instructions will be added when there is a working version.

## Possible Future Improvements

- Add city search instead of a fixed city list.
- Support outings that continue past midnight.
- Let users adjust their own temperature cutoffs.
- Compare two destinations for a day trip.

## License

The project code is licensed under the MIT License. Weather data remains subject to its source licenses and attribution requirements.
