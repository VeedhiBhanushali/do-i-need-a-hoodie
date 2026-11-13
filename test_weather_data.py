import unittest

from weather_data import make_hourly_rows


class WeatherDataTests(unittest.TestCase):
    def setUp(self):
        self.sample = {
            "hourly": {
                "time": ["2026-11-13T09:00", "2026-11-13T10:00"],
                "temperature_2m": [15.2, 16.0],
                "apparent_temperature": [14.1, 15.0],
                "precipitation_probability": [20, 30],
                "wind_speed_10m": [8.4, 9.1],
            }
        }

    def test_makes_one_row_for_each_hour(self):
        rows = make_hourly_rows(self.sample)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["feels_like_c"], 14.1)

    def test_keeps_missing_values_as_none(self):
        self.sample["hourly"]["apparent_temperature"][0] = None

        rows = make_hourly_rows(self.sample)

        self.assertIsNone(rows[0]["feels_like_c"])

    def test_rejects_a_missing_field(self):
        del self.sample["hourly"]["wind_speed_10m"]

        with self.assertRaises(ValueError):
            make_hourly_rows(self.sample)

    def test_rejects_lists_with_different_lengths(self):
        self.sample["hourly"]["temperature_2m"].pop()

        with self.assertRaises(ValueError):
            make_hourly_rows(self.sample)


if __name__ == "__main__":
    unittest.main()
