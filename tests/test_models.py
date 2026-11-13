"""Tests for forecast data validation."""

from datetime import datetime, timezone
import unittest

from hoodie.models import ForecastDataset, ForecastRecord, ForecastValidationError


def make_record(hour: int = 9, **overrides: object) -> ForecastRecord:
    values: dict[str, object] = {
        "local_time": datetime(2026, 11, 13, hour),
        "temperature_c": 15.2,
        "apparent_temperature_c": 14.1,
        "precipitation_probability_pct": 25,
        "wind_speed_kmh": 8.4,
    }
    values.update(overrides)
    return ForecastRecord(**values)  # type: ignore[arg-type]


class ForecastRecordTests(unittest.TestCase):
    def test_builds_record_from_open_meteo_values(self) -> None:
        record = ForecastRecord.from_open_meteo(
            local_time="2026-11-13T09:00",
            temperature_c=15,
            apparent_temperature_c=14.1,
            precipitation_probability_pct=25,
            wind_speed_kmh=8.4,
        )

        self.assertEqual(record.local_time, datetime(2026, 11, 13, 9))
        self.assertEqual(record.temperature_c, 15.0)

    def test_preserves_missing_measurements(self) -> None:
        record = make_record(apparent_temperature_c=None)

        self.assertIsNone(record.apparent_temperature_c)

    def test_rejects_invalid_precipitation_probability(self) -> None:
        with self.assertRaisesRegex(ForecastValidationError, "between 0 and 100"):
            make_record(precipitation_probability_pct=101)

    def test_rejects_negative_wind_speed(self) -> None:
        with self.assertRaisesRegex(ForecastValidationError, "cannot be negative"):
            make_record(wind_speed_kmh=-0.1)

    def test_rejects_non_finite_numbers(self) -> None:
        with self.assertRaisesRegex(ForecastValidationError, "must be finite"):
            make_record(temperature_c=float("nan"))


class ForecastDatasetTests(unittest.TestCase):
    def test_accepts_ordered_unique_records(self) -> None:
        dataset = ForecastDataset.from_records(
            city=" San Jose ",
            latitude=37.3382,
            longitude=-121.8863,
            timezone=" America/Los_Angeles ",
            downloaded_at=datetime(2026, 11, 13, 17, tzinfo=timezone.utc),
            records=(make_record(9), make_record(10)),
        )

        self.assertEqual(dataset.city, "San Jose")
        self.assertEqual(dataset.timezone, "America/Los_Angeles")
        self.assertEqual(len(dataset.records), 2)

    def test_rejects_out_of_order_records(self) -> None:
        with self.assertRaisesRegex(ForecastValidationError, "ordered"):
            ForecastDataset.from_records(
                city="San Jose",
                latitude=37.3382,
                longitude=-121.8863,
                timezone="America/Los_Angeles",
                downloaded_at=datetime.now(timezone.utc),
                records=(make_record(10), make_record(9)),
            )

    def test_rejects_duplicate_timestamps(self) -> None:
        with self.assertRaisesRegex(ForecastValidationError, "duplicate"):
            ForecastDataset.from_records(
                city="San Jose",
                latitude=37.3382,
                longitude=-121.8863,
                timezone="America/Los_Angeles",
                downloaded_at=datetime.now(timezone.utc),
                records=(make_record(9), make_record(9)),
            )

    def test_rejects_empty_record_collection(self) -> None:
        with self.assertRaisesRegex(ForecastValidationError, "cannot be empty"):
            ForecastDataset.from_records(
                city="San Jose",
                latitude=37.3382,
                longitude=-121.8863,
                timezone="America/Los_Angeles",
                downloaded_at=datetime.now(timezone.utc),
                records=(),
            )


if __name__ == "__main__":
    unittest.main()
