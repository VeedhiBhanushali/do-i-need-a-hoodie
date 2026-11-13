"""Small helpers for working with the Open-Meteo hourly response."""

HOURLY_FIELDS = [
    "time",
    "temperature_2m",
    "apparent_temperature",
    "precipitation_probability",
    "wind_speed_10m",
]


def make_hourly_rows(api_response):
    """Turn Open-Meteo's hourly lists into one dictionary per hour."""

    hourly = api_response.get("hourly")
    if not hourly:
        raise ValueError("The response does not have hourly weather data.")

    missing = [field for field in HOURLY_FIELDS if field not in hourly]
    if missing:
        raise ValueError(f"Missing hourly field: {missing[0]}")

    lengths = [len(hourly[field]) for field in HOURLY_FIELDS]
    if len(set(lengths)) != 1:
        raise ValueError("The hourly weather lists are not the same length.")

    rows = []
    for index in range(lengths[0]):
        rows.append(
            {
                "time": hourly["time"][index],
                "temperature_c": hourly["temperature_2m"][index],
                "feels_like_c": hourly["apparent_temperature"][index],
                "precipitation_probability": hourly["precipitation_probability"][index],
                "wind_speed_kmh": hourly["wind_speed_10m"][index],
            }
        )

    return rows
