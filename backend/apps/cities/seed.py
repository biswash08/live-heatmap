"""Seed metadata for Nepal cities used by the live heatmap backend."""

from __future__ import annotations

KATHMANDU_CITY_ID = 'ktm'
LALITPUR_CITY_ID = 'lpt'
BHAKTAPUR_CITY_ID = 'bkt'

# Municipality-level coverage for Kathmandu, Lalitpur and Bhaktapur districts.
KATHMANDU_MUNICIPALITIES = {
    'ktm': {
        'id': 'ktm',
        'slug': 'kathmandu-metropolitan-city',
        'name': 'Kathmandu Metropolitan City',
        'country': 'Nepal',
        'district': 'Kathmandu',
        'lat': 27.7172,
        'lng': 85.324,
        'default_h3_resolution': 8,
        'bounds': {'north': 27.8, 'south': 27.6, 'east': 85.45, 'west': 85.2},
        'streets': [
            'New Baneshwor',
            'Tripureshwor',
            'Durbarmarg',
            'Thamel',
            'Koteshwor',
            'Bhatbhateni',
            'Maharajgunj',
            'Balaju',
            'Ason',
            'Gongabu',
        ],
    },
    'kmc': {
        'id': 'kmc',
        'slug': 'kathmandu-metropolitan-city-east',
        'name': 'Kathmandu Metropolitan City (East)',
        'country': 'Nepal',
        'district': 'Kathmandu',
        'lat': 27.70,
        'lng': 85.33,
        'default_h3_resolution': 8,
        'bounds': {'north': 27.74, 'south': 27.68, 'east': 85.36, 'west': 85.29},
        'streets': [
            'Sinamangal',
            'Chabahil',
            'Jorpati',
            'Gairidhara',
            'Lazimpat',
        ],
    },
    'kaw': {
        'id': 'kaw',
        'slug': 'kathmandu-west',
        'name': 'Kathmandu West',
        'country': 'Nepal',
        'district': 'Kathmandu',
        'lat': 27.71,
        'lng': 85.31,
        'default_h3_resolution': 8,
        'bounds': {'north': 27.75, 'south': 27.68, 'east': 85.34, 'west': 85.28},
        'streets': [
            'Maharajgunj',
            'Sukedhara',
            'Bishalnagar',
            'Kalimati',
            'Samakhushi',
        ],
    },
}

LALITPUR_MUNICIPALITIES = {
    'lpt': {
        'id': 'lpt',
        'slug': 'lalitpur-metropolitan-city',
        'name': 'Lalitpur Metropolitan City',
        'country': 'Nepal',
        'district': 'Lalitpur',
        'lat': 27.6684,
        'lng': 85.3206,
        'default_h3_resolution': 8,
        'bounds': {'north': 27.7, 'south': 27.6, 'east': 85.38, 'west': 85.28},
        'streets': [
            'Satdobato',
            'Lagankhel',
            'Lubhu',
            'Ekantakuna',
            'Kalimati',
            'Patan Durbar',
            'Gwarko',
        ],
    },
    'tap': {
        'id': 'tap',
        'slug': 'thankot',
        'name': 'Thankot',
        'country': 'Nepal',
        'district': 'Lalitpur',
        'lat': 27.668,
        'lng': 85.27,
        'default_h3_resolution': 8,
        'bounds': {'north': 27.69, 'south': 27.65, 'east': 85.30, 'west': 85.25},
        'streets': ['Thankot Road', 'Godam', 'Pani Pati'],
    },
    'mat': {
        'id': 'mat',
        'slug': 'madhyapur-thimi',
        'name': 'Madhyapur Thimi',
        'country': 'Nepal',
        'district': 'Lalitpur',
        'lat': 27.675,
        'lng': 85.37,
        'default_h3_resolution': 8,
        'bounds': {'north': 27.71, 'south': 27.65, 'east': 85.39, 'west': 85.34},
        'streets': ['Thimi Bazar', 'Madhyapur', 'Bode', 'Nayabazar'],
    },
}

BHAKTAPUR_MUNICIPALITIES = {
    'bkt': {
        'id': 'bkt',
        'slug': 'bhaktapur-metropolitan-city',
        'name': 'Bhaktapur Metropolitan City',
        'country': 'Nepal',
        'district': 'Bhaktapur',
        'lat': 27.671,
        'lng': 85.429,
        'default_h3_resolution': 8,
        'bounds': {'north': 27.71, 'south': 27.64, 'east': 85.47, 'west': 85.39},
        'streets': [
            'Dattatraya Square',
            'Taumadhi Square',
            'Siddhi Laxmi',
            'Bhaktapur Durbar',
            'Suek',
        ],
    },
    'sud': {
        'id': 'sud',
        'slug': 'suryabinayak',
        'name': 'Suryabinayak',
        'country': 'Nepal',
        'district': 'Bhaktapur',
        'lat': 27.64,
        'lng': 85.41,
        'default_h3_resolution': 8,
        'bounds': {'north': 27.67, 'south': 27.62, 'east': 85.44, 'west': 85.39},
        'streets': ['Suryabinayak Road', 'Madhyapur', 'Balkumari'],
    },
    'cha': {
        'id': 'cha',
        'slug': 'changunarayan',
        'name': 'Changunarayan',
        'country': 'Nepal',
        'district': 'Bhaktapur',
        'lat': 27.72,
        'lng': 85.43,
        'default_h3_resolution': 8,
        'bounds': {'north': 27.75, 'south': 27.70, 'east': 85.47, 'west': 85.41},
        'streets': ['Changunarayan Temple Road', 'Bageshwori', 'Nala'],
    },
}

KATHMANDU_CITY = KATHMANDU_MUNICIPALITIES['ktm']
LALITPUR_CITY = LALITPUR_MUNICIPALITIES['lpt']
BHAKTAPUR_CITY = BHAKTAPUR_MUNICIPALITIES['bkt']

CITY_SEED = {
    **KATHMANDU_MUNICIPALITIES,
    **LALITPUR_MUNICIPALITIES,
    **BHAKTAPUR_MUNICIPALITIES,
}


def get_city_by_id(city_id: str | None) -> dict | None:
    if city_id is None:
        return None
    return CITY_SEED.get(city_id)


def get_city_streets(city_id: str | None) -> list[str]:
    city = get_city_by_id(city_id)
    if city is None:
        return []
    return city.get('streets', [])


def get_default_city() -> dict:
    return KATHMANDU_CITY
