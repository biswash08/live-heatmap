"""Seed metadata for Nepal cities used by the live heatmap backend."""

from __future__ import annotations

KATHMANDU_CITY_ID = 'ktm'
LALITPUR_CITY_ID = 'lpt'
BHAKTAPUR_CITY_ID = 'bkt'

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

LALITPUR_CITY = {
    'id': LALITPUR_CITY_ID,
    'slug': 'lalitpur',
    'name': 'Lalitpur',
    'country': 'Nepal',
    'lat': 27.6684,
    'lng': 85.3206,
    'default_h3_resolution': 8,
    'bounds': {
        'north': 27.7,
        'south': 27.6,
        'east': 85.38,
        'west': 85.28,
    },
}

BHAKTAPUR_CITY = {
    'id': BHAKTAPUR_CITY_ID,
    'slug': 'bhaktapur',
    'name': 'Bhaktapur',
    'country': 'Nepal',
    'lat': 27.671,
    'lng': 85.429,
    'default_h3_resolution': 8,
    'bounds': {
        'north': 27.71,
        'south': 27.64,
        'east': 85.47,
        'west': 85.39,
    },
}

CITY_SEED = {
    KATHMANDU_CITY_ID: KATHMANDU_CITY,
    LALITPUR_CITY_ID: LALITPUR_CITY,
    BHAKTAPUR_CITY_ID: BHAKTAPUR_CITY,
}


def get_city_by_id(city_id: str | None) -> dict | None:
    if city_id is None:
        return None
    return CITY_SEED.get(city_id)


def get_default_city() -> dict:
    return KATHMANDU_CITY
