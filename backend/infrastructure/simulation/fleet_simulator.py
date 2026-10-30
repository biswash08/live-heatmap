"""Helpers for generating realistic fleet movement events for the live heatmap backend."""

from __future__ import annotations

from typing import Any

from infrastructure.redis.state_store import DriverStateStore
from workers.location_processor import process_location_event


def build_location_event(
    driver_id: str,
    city_id: str,
    latitude: float,
    longitude: float,
    event_version: int,
    timestamp_epoch: float,
    availability_status: str = 'online',
) -> dict[str, Any]:
    return {
        'event_id': f'{driver_id}:{event_version}:{int(timestamp_epoch)}',
        'driver_id': driver_id,
        'city_id': city_id,
        'latitude': latitude,
        'longitude': longitude,
        'timestamp_epoch': timestamp_epoch,
        'event_version': event_version,
        'availability_status': availability_status,
    }


def simulate_driver_path(
    driver_id: str,
    city_id: str,
    waypoints: list[tuple[float, float]],
    state_store: DriverStateStore | None = None,
    start_time: float = 1_700_000_000.0,
    interval_seconds: int = 5,
) -> list[dict[str, Any]]:
    store = state_store or DriverStateStore()
    events: list[dict[str, Any]] = []

    for index, (lat, lon) in enumerate(waypoints, start=1):
        event_time = start_time + index * interval_seconds
        event = build_location_event(
            driver_id=driver_id,
            city_id=city_id,
            latitude=lat,
            longitude=lon,
            event_version=index,
            timestamp_epoch=event_time,
        )
        result = process_location_event(event, store)
        events.append(result)

    return events


def simulate_fleet(
    city_id: str,
    driver_points: dict[str, list[tuple[float, float]]],
    state_store: DriverStateStore | None = None,
    start_time: float = 1_700_000_000.0,
    interval_seconds: int = 5,
) -> dict[str, list[dict[str, Any]]]:
    store = state_store or DriverStateStore()
    simulation: dict[str, list[dict[str, Any]]] = {}

    for driver_id, waypoints in driver_points.items():
        simulation[driver_id] = simulate_driver_path(
            driver_id=driver_id,
            city_id=city_id,
            waypoints=waypoints,
            state_store=store,
            start_time=start_time,
            interval_seconds=interval_seconds,
        )

    return simulation
