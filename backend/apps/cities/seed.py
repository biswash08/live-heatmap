"""Seed metadata for Nepal cities used by the live heatmap backend."""

from __future__ import annotations

KATHMANDU_CITY_ID = 'ktm'

KATHMANDU_CITY = {
    'id': KATHMANDU_CITY_ID,
    'slug': 'kathmandu',
    'name': 'Kathmandu',
    'country': 'Nepal',
    'lat': 27.7172,
    'lng': 85.324,
    'default_h3_resolution': 8,
    'bounds': {
        'north': 27.8,
        'south': 27.6,
        'east': 85.45,
        'west': 85.2,
    },
}

CITY_SEED = {
    KATHMANDU_CITY_ID: KATHMANDU_CITY,
}


def get_city_by_id(city_id: str | None) -> dict | None:
    if city_id is None:
        return None
    return CITY_SEED.get(city_id)


def get_default_city() -> dict:
    return KATHMANDU_CITY
