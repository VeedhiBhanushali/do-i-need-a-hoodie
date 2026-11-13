"""Validated data structures shared by the API, storage, and analysis layers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import math
from numbers import Real
from typing import Any, Iterable


class ForecastValidationError(ValueError):
    """Raised when forecast data cannot be used safely by the application."""


def _optional_number(value: Any, field_name: str) -> float | None:
    """Return a finite float while preserving an API's missing values as None."""

    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ForecastValidationError(f"{field_name} must be a number or None")

    result = float(value)
    if not math.isfinite(result):
        raise ForecastValidationError(f"{field_name} must be finite")
    return result


@dataclass(frozen=True, slots=True)
class ForecastRecord:
    """One hourly forecast observation in a city's local time."""

    local_time: datetime
    temperature_c: float | None
    apparent_temperature_c: float | None
    precipitation_probability_pct: float | None
    wind_speed_kmh: float | None

    def __post_init__(self) -> None:
        if not isinstance(self.local_time, datetime):
            raise ForecastValidationError("local_time must be a datetime")

        numeric_fields = (
            "temperature_c",
            "apparent_temperature_c",
            "precipitation_probability_pct",
            "wind_speed_kmh",
        )
        for field_name in numeric_fields:
            normalized = _optional_number(getattr(self, field_name), field_name)
            object.__setattr__(self, field_name, normalized)

        precipitation = self.precipitation_probability_pct
        if precipitation is not None and not 0 <= precipitation <= 100:
            raise ForecastValidationError(
                "precipitation_probability_pct must be between 0 and 100"
            )

        wind_speed = self.wind_speed_kmh
        if wind_speed is not None and wind_speed < 0:
            raise ForecastValidationError("wind_speed_kmh cannot be negative")

    @classmethod
    def from_open_meteo(
        cls,
        *,
        local_time: str,
        temperature_c: Any,
        apparent_temperature_c: Any,
        precipitation_probability_pct: Any,
        wind_speed_kmh: Any,
    ) -> ForecastRecord:
        """Build a record from values in an Open-Meteo hourly response."""

        try:
            parsed_time = datetime.fromisoformat(local_time)
        except (TypeError, ValueError) as exc:
            raise ForecastValidationError(
                f"invalid Open-Meteo timestamp: {local_time!r}"
            ) from exc

        return cls(
            local_time=parsed_time,
            temperature_c=temperature_c,
            apparent_temperature_c=apparent_temperature_c,
            precipitation_probability_pct=precipitation_probability_pct,
            wind_speed_kmh=wind_speed_kmh,
        )


@dataclass(frozen=True, slots=True)
class ForecastDataset:
    """Metadata and ordered hourly records for one downloaded forecast."""

    city: str
    latitude: float
    longitude: float
    timezone: str
    downloaded_at: datetime
    records: tuple[ForecastRecord, ...]
    source: str = "Open-Meteo"

    def __post_init__(self) -> None:
        city = self.city.strip() if isinstance(self.city, str) else ""
        timezone = self.timezone.strip() if isinstance(self.timezone, str) else ""
        if not city:
            raise ForecastValidationError("city cannot be blank")
        if not timezone:
            raise ForecastValidationError("timezone cannot be blank")
        if not isinstance(self.downloaded_at, datetime):
            raise ForecastValidationError("downloaded_at must be a datetime")

        latitude = _optional_number(self.latitude, "latitude")
        longitude = _optional_number(self.longitude, "longitude")
        if latitude is None or not -90 <= latitude <= 90:
            raise ForecastValidationError("latitude must be between -90 and 90")
        if longitude is None or not -180 <= longitude <= 180:
            raise ForecastValidationError("longitude must be between -180 and 180")

        records = tuple(self.records)
        if not records:
            raise ForecastValidationError("records cannot be empty")
        if any(not isinstance(record, ForecastRecord) for record in records):
            raise ForecastValidationError("records must contain ForecastRecord objects")

        times = [record.local_time for record in records]
        if times != sorted(times):
            raise ForecastValidationError("records must be ordered by local_time")
        if len(times) != len(set(times)):
            raise ForecastValidationError("records cannot contain duplicate timestamps")

        object.__setattr__(self, "city", city)
        object.__setattr__(self, "timezone", timezone)
        object.__setattr__(self, "latitude", latitude)
        object.__setattr__(self, "longitude", longitude)
        object.__setattr__(self, "records", records)

    @classmethod
    def from_records(
        cls,
        *,
        city: str,
        latitude: float,
        longitude: float,
        timezone: str,
        downloaded_at: datetime,
        records: Iterable[ForecastRecord],
    ) -> ForecastDataset:
        """Create a dataset while accepting any iterable of records."""

        return cls(
            city=city,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            downloaded_at=downloaded_at,
            records=tuple(records),
        )

