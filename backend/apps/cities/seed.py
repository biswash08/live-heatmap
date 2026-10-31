"""Seed metadata for Nepal cities used by the live heatmap backend."""

from __future__ import annotations

import math
import re

KATHMANDU_CITY_ID = 'ktm'
LALITPUR_CITY_ID = 'lpt'
BHAKTAPUR_CITY_ID = 'bkt'

# Municipality-level coverage for Kathmandu, Lalitpur and Bhaktapur districts.
KATHMANDU_MUNICIPALITIES = {
    'ktm': {
        'id': 'ktm',
        'slug': 'kathmandu-metropolitan-city',
        'name': 'Kathmandu Metropolitan City',
        'province': 'Bagmati Province',
        'country': 'Nepal',
        'district': 'Kathmandu',
        'municipality': 'Kathmandu Metropolitan City',
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
        'province': 'Bagmati Province',
        'country': 'Nepal',
        'district': 'Kathmandu',
        'municipality': 'Kathmandu Metropolitan City',
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
        'province': 'Bagmati Province',
        'country': 'Nepal',
        'district': 'Kathmandu',
        'municipality': 'Kathmandu Metropolitan City',
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
        'province': 'Bagmati Province',
        'country': 'Nepal',
        'district': 'Lalitpur',
        'municipality': 'Lalitpur Metropolitan City',
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
        'province': 'Bagmati Province',
        'country': 'Nepal',
        'district': 'Lalitpur',
        'municipality': 'Thankot',
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
        'province': 'Bagmati Province',
        'country': 'Nepal',
        'district': 'Lalitpur',
        'municipality': 'Madhyapur Thimi',
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
        'province': 'Bagmati Province',
        'country': 'Nepal',
        'district': 'Bhaktapur',
        'municipality': 'Bhaktapur Metropolitan City',
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
        'province': 'Bagmati Province',
        'country': 'Nepal',
        'district': 'Bhaktapur',
        'municipality': 'Suryabinayak',
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
        'province': 'Bagmati Province',
        'country': 'Nepal',
        'district': 'Bhaktapur',
        'municipality': 'Changunarayan',
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

CITY_ADDRESS_INDEX = {
    'ktm': [
        {
            'id': 'ktm-baluwatar-ward-10',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 10',
            'area': 'Baluwatar',
            'street': 'Baluwatar Road',
            'landmark': 'Baluwatar Community Hall',
            'latitude': 27.7172,
            'longitude': 85.3231,
            'place_type': 'residential',
            'formatted_address': 'Baluwatar Road, Ward 10, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['baluwatar', 'ward 10', 'kathmandu', 'metropolitan city'],
        },
        {
            'id': 'ktm-thamel-ward-15',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 15',
            'area': 'Thamel',
            'street': 'Thamel Marg',
            'landmark': 'Hotel Himalaya',
            'latitude': 27.7145,
            'longitude': 85.3117,
            'place_type': 'tourist_hub',
            'formatted_address': 'Thamel Marg, Ward 15, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['thamel', 'ward 15', 'tourist', 'kathmandu'],
        },
        {
            'id': 'ktm-baneshwor-ward-32',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 32',
            'area': 'New Baneshwor',
            'street': 'New Baneshwor Road',
            'landmark': 'Baneshwor Plaza',
            'latitude': 27.6869,
            'longitude': 85.3400,
            'place_type': 'commercial',
            'formatted_address': 'New Baneshwor Road, Ward 32, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['new baneshwor', 'baneshwor', 'ward 32', 'kathmandu'],
        },
        {
            'id': 'ktm-koteshwor-ward-28',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 28',
            'area': 'Koteshwor',
            'street': 'Koteshwor Ring Road',
            'landmark': 'Koteshwor Hospital',
            'latitude': 27.6764,
            'longitude': 85.3472,
            'place_type': 'residential',
            'formatted_address': 'Koteshwor Ring Road, Ward 28, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['koteshwor', 'ring road', 'ward 28', 'kathmandu'],
        },
        {
            'id': 'ktm-bhatbhateni-ward-10',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 10',
            'area': 'Bhatbhateni',
            'street': 'Bhatbhateni Marg',
            'landmark': 'Bhatbhateni Supermarket',
            'latitude': 27.7005,
            'longitude': 85.3258,
            'place_type': 'commercial',
            'formatted_address': 'Bhatbhateni Marg, Ward 10, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['bhatbhateni', 'ward 10', 'grocery', 'kathmandu'],
        },
        {
            'id': 'ktm-tripureshwor-ward-3',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 3',
            'area': 'Tripureshwor',
            'street': 'Pashupatinath Road',
            'landmark': 'Tripureshwor Temple',
            'latitude': 27.7050,
            'longitude': 85.3148,
            'place_type': 'religious',
            'formatted_address': 'Pashupatinath Road, Ward 3, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['tripureshwor', 'ward 3', 'temple', 'kathmandu'],
        },
        {
            'id': 'ktm-maharajgunj-ward-8',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 8',
            'area': 'Maharajgunj',
            'street': 'Maharajgunj Road',
            'landmark': 'Maharajgunj Health Post',
            'latitude': 27.7532,
            'longitude': 85.3275,
            'place_type': 'residential',
            'formatted_address': 'Maharajgunj Road, Ward 8, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['maharajgunj', 'ward 8', 'kathmandu'],
        },
        {
            'id': 'ktm-gongabu-ward-17',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 17',
            'area': 'Gongabu',
            'street': 'Gongabu Bus Park Road',
            'landmark': 'Gongabu Bus Park',
            'latitude': 27.7286,
            'longitude': 85.3027,
            'place_type': 'transport',
            'formatted_address': 'Gongabu Bus Park Road, Ward 17, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['gongabu', 'bus park', 'ward 17', 'kathmandu'],
        },
        {
            'id': 'ktm-lazimpat-ward-4',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 4',
            'area': 'Lazimpat',
            'street': 'Lazimpat Road',
            'landmark': 'Lazimpat Park',
            'latitude': 27.7230,
            'longitude': 85.3251,
            'place_type': 'residential',
            'formatted_address': 'Lazimpat Road, Ward 4, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['lazimpat', 'ward 4', 'park', 'kathmandu'],
        },
        {
            'id': 'ktm-pashupatinath-ward-8',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 8',
            'area': 'Guheshwori',
            'street': 'Pashupatinath Road',
            'landmark': 'Pashupatinath Temple',
            'latitude': 27.7104,
            'longitude': 85.3461,
            'place_type': 'religious',
            'formatted_address': 'Pashupatinath Road, Ward 8, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['pashupatinath', 'temple', 'ward 8', 'kathmandu'],
        },
        {
            'id': 'ktm-boudhanath-ward-12',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 12',
            'area': 'Boudhanath',
            'street': 'Boudha Road',
            'landmark': 'Boudhanath Stupa',
            'latitude': 27.7211,
            'longitude': 85.3593,
            'place_type': 'religious',
            'formatted_address': 'Boudha Road, Ward 12, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['boudhanath', 'stupa', 'ward 12', 'kathmandu'],
        },
        {
            'id': 'ktm-swayambhunath-ward-4',
            'city_id': 'ktm',
            'province': 'Bagmati Province',
            'district': 'Kathmandu',
            'municipality': 'Kathmandu Metropolitan City',
            'ward': 'Ward 4',
            'area': 'Swayambhu',
            'street': 'Swayambhu Road',
            'landmark': 'Swayambhunath Stupa',
            'latitude': 27.7149,
            'longitude': 85.2898,
            'place_type': 'religious',
            'formatted_address': 'Swayambhu Road, Ward 4, Kathmandu Metropolitan City, Kathmandu, Bagmati Province, Nepal',
            'search_terms': ['swayambhunath', 'monkey temple', 'stupa', 'ward 4', 'kathmandu'],
        },
    ],
    'lpt': [
        {
            'id': 'lpt-lagankhel-ward-7',
            'city_id': 'lpt',
            'province': 'Bagmati Province',
            'district': 'Lalitpur',
            'municipality': 'Lalitpur Metropolitan City',
            'ward': 'Ward 7',
            'area': 'Lagankhel',
            'street': 'Lagankhel Road',
            'landmark': 'Patan Hospital',
            'latitude': 27.6637,
            'longitude': 85.3245,
            'place_type': 'medical',
            'formatted_address': 'Lagankhel Road, Ward 7, Lalitpur Metropolitan City, Lalitpur, Bagmati Province, Nepal',
            'search_terms': ['lagankhel', 'ward 7', 'lalitpur'],
        },
        {
            'id': 'lpt-satdobato-ward-6',
            'city_id': 'lpt',
            'province': 'Bagmati Province',
            'district': 'Lalitpur',
            'municipality': 'Lalitpur Metropolitan City',
            'ward': 'Ward 6',
            'area': 'Satdobato',
            'street': 'Satdobato Road',
            'landmark': 'Satdobato Chowk',
            'latitude': 27.6504,
            'longitude': 85.3230,
            'place_type': 'residential',
            'formatted_address': 'Satdobato Road, Ward 6, Lalitpur Metropolitan City, Lalitpur, Bagmati Province, Nepal',
            'search_terms': ['satdobato', 'ward 6', 'lalitpur'],
        },
        {
            'id': 'lpt-gwarko-ward-14',
            'city_id': 'lpt',
            'province': 'Bagmati Province',
            'district': 'Lalitpur',
            'municipality': 'Lalitpur Metropolitan City',
            'ward': 'Ward 14',
            'area': 'Gwarko',
            'street': 'Gwarko Chowk Road',
            'landmark': 'Gwarko Chowk',
            'latitude': 27.6509,
            'longitude': 85.3378,
            'place_type': 'commercial',
            'formatted_address': 'Gwarko Chowk Road, Ward 14, Lalitpur Metropolitan City, Lalitpur, Bagmati Province, Nepal',
            'search_terms': ['gwarko', 'chowk', 'ward 14', 'lalitpur'],
        },
        {
            'id': 'lpt-lubhu-ward-20',
            'city_id': 'lpt',
            'province': 'Bagmati Province',
            'district': 'Lalitpur',
            'municipality': 'Lalitpur Metropolitan City',
            'ward': 'Ward 20',
            'area': 'Lubhu',
            'street': 'Lubhu Road',
            'landmark': 'Lubhu Temple Area',
            'latitude': 27.6332,
            'longitude': 85.3381,
            'place_type': 'residential',
            'formatted_address': 'Lubhu Road, Ward 20, Lalitpur Metropolitan City, Lalitpur, Bagmati Province, Nepal',
            'search_terms': ['lubhu', 'ward 20', 'lalitpur'],
        },
        {
            'id': 'lpt-patan-durbar-ward-3',
            'city_id': 'lpt',
            'province': 'Bagmati Province',
            'district': 'Lalitpur',
            'municipality': 'Lalitpur Metropolitan City',
            'ward': 'Ward 3',
            'area': 'Patan',
            'street': 'Patan Durbar Road',
            'landmark': 'Patan Durbar Square',
            'latitude': 27.6710,
            'longitude': 85.3248,
            'place_type': 'heritage',
            'formatted_address': 'Patan Durbar Road, Ward 3, Lalitpur Metropolitan City, Lalitpur, Bagmati Province, Nepal',
            'search_terms': ['patan durbar', 'durbar square', 'ward 3', 'lalitpur'],
        },
        {
            'id': 'lpt-kupondole-ward-5',
            'city_id': 'lpt',
            'province': 'Bagmati Province',
            'district': 'Lalitpur',
            'municipality': 'Lalitpur Metropolitan City',
            'ward': 'Ward 5',
            'area': 'Kupondole',
            'street': 'Kupondole Road',
            'landmark': 'Kupondole Chowk',
            'latitude': 27.6661,
            'longitude': 85.3184,
            'place_type': 'commercial',
            'formatted_address': 'Kupondole Road, Ward 5, Lalitpur Metropolitan City, Lalitpur, Bagmati Province, Nepal',
            'search_terms': ['kupondole', 'chowk', 'ward 5', 'lalitpur'],
        },
        {
            'id': 'lpt-jawalakhel-ward-2',
            'city_id': 'lpt',
            'province': 'Bagmati Province',
            'district': 'Lalitpur',
            'municipality': 'Lalitpur Metropolitan City',
            'ward': 'Ward 2',
            'area': 'Jawalakhel',
            'street': 'Jawalakhel Road',
            'landmark': 'Jawalakhel Park',
            'latitude': 27.6668,
            'longitude': 85.3127,
            'place_type': 'park',
            'formatted_address': 'Jawalakhel Road, Ward 2, Lalitpur Metropolitan City, Lalitpur, Bagmati Province, Nepal',
            'search_terms': ['jawalakhel', 'park', 'ward 2', 'lalitpur'],
        },
    ],
    'bkt': [
        {
            'id': 'bkt-taumadhi-ward-5',
            'city_id': 'bkt',
            'province': 'Bagmati Province',
            'district': 'Bhaktapur',
            'municipality': 'Bhaktapur Metropolitan City',
            'ward': 'Ward 5',
            'area': 'Taumadhi',
            'street': 'Taumadhi Square Road',
            'landmark': 'Taumadhi Square',
            'latitude': 27.6723,
            'longitude': 85.4287,
            'place_type': 'heritage',
            'formatted_address': 'Taumadhi Square Road, Ward 5, Bhaktapur Metropolitan City, Bhaktapur, Bagmati Province, Nepal',
            'search_terms': ['taumadhi', 'square', 'ward 5', 'bhaktapur'],
        },
        {
            'id': 'bkt-siddhi-laxmi-ward-3',
            'city_id': 'bkt',
            'province': 'Bagmati Province',
            'district': 'Bhaktapur',
            'municipality': 'Bhaktapur Metropolitan City',
            'ward': 'Ward 3',
            'area': 'Siddhi Laxmi',
            'street': 'Siddhi Laxmi Road',
            'landmark': 'Siddhi Laxmi Temple',
            'latitude': 27.6735,
            'longitude': 85.4255,
            'place_type': 'religious',
            'formatted_address': 'Siddhi Laxmi Road, Ward 3, Bhaktapur Metropolitan City, Bhaktapur, Bagmati Province, Nepal',
            'search_terms': ['siddhi laxmi', 'ward 3', 'bhaktapur'],
        },
        {
            'id': 'bkt-dattatraya-ward-2',
            'city_id': 'bkt',
            'province': 'Bagmati Province',
            'district': 'Bhaktapur',
            'municipality': 'Bhaktapur Metropolitan City',
            'ward': 'Ward 2',
            'area': 'Dattatraya',
            'street': 'Dattatraya Square Road',
            'landmark': 'Dattatraya Square',
            'latitude': 27.6698,
            'longitude': 85.4302,
            'place_type': 'heritage',
            'formatted_address': 'Dattatraya Square Road, Ward 2, Bhaktapur Metropolitan City, Bhaktapur, Bagmati Province, Nepal',
            'search_terms': ['dattatraya', 'square', 'ward 2', 'bhaktapur'],
        },
        {
            'id': 'bkt-duwakot-ward-7',
            'city_id': 'bkt',
            'province': 'Bagmati Province',
            'district': 'Bhaktapur',
            'municipality': 'Bhaktapur Metropolitan City',
            'ward': 'Ward 7',
            'area': 'Duwakot',
            'street': 'Duwakot Road',
            'landmark': 'Duwakot Chowk',
            'latitude': 27.6812,
            'longitude': 85.4231,
            'place_type': 'residential',
            'formatted_address': 'Duwakot Road, Ward 7, Bhaktapur Metropolitan City, Bhaktapur, Bagmati Province, Nepal',
            'search_terms': ['duwakot', 'ward 7', 'chowk', 'bhaktapur'],
        },
        {
            'id': 'bkt-bajeko-nilo-pul-ward-8',
            'city_id': 'bkt',
            'province': 'Bagmati Province',
            'district': 'Bhaktapur',
            'municipality': 'Bhaktapur Metropolitan City',
            'ward': 'Ward 8',
            'area': 'Bajeko Nilo Pul',
            'street': 'Bajeko Nilo Pul Road',
            'landmark': 'Bajeko Nilo Pul',
            'latitude': 27.6758,
            'longitude': 85.4316,
            'place_type': 'transport',
            'formatted_address': 'Bajeko Nilo Pul Road, Ward 8, Bhaktapur Metropolitan City, Bhaktapur, Bagmati Province, Nepal',
            'search_terms': ['bajeko nilo pul', 'nilo pul', 'ward 8', 'bhaktapur'],
        },
        {
            'id': 'bkt-manau-bakery-ward-5',
            'city_id': 'bkt',
            'province': 'Bagmati Province',
            'district': 'Bhaktapur',
            'municipality': 'Bhaktapur Metropolitan City',
            'ward': 'Ward 5',
            'area': 'Taumadhi',
            'street': 'Taumadhi Square Road',
            'landmark': 'Manau Bakery',
            'latitude': 27.6722,
            'longitude': 85.4289,
            'place_type': 'food',
            'formatted_address': 'Taumadhi Square Road, Ward 5, Bhaktapur Metropolitan City, Bhaktapur, Bagmati Province, Nepal',
            'search_terms': ['manau bakery', 'taumadhi', 'bakery', 'ward 5', 'bhaktapur'],
        },
        {
            'id': 'bkt-bhaktapur-durbar-ward-1',
            'city_id': 'bkt',
            'province': 'Bagmati Province',
            'district': 'Bhaktapur',
            'municipality': 'Bhaktapur Metropolitan City',
            'ward': 'Ward 1',
            'area': 'Bhaktapur Durbar',
            'street': 'Bhaktapur Durbar Road',
            'landmark': 'Bhaktapur Durbar Square',
            'latitude': 27.6720,
            'longitude': 85.4297,
            'place_type': 'heritage',
            'formatted_address': 'Bhaktapur Durbar Road, Ward 1, Bhaktapur Metropolitan City, Bhaktapur, Bagmati Province, Nepal',
            'search_terms': ['bhaktapur durbar', 'durbar square', 'ward 1', 'bhaktapur'],
        },
        {
            'id': 'bkt-changu-narayan-ward-10',
            'city_id': 'bkt',
            'province': 'Bagmati Province',
            'district': 'Bhaktapur',
            'municipality': 'Bhaktapur Metropolitan City',
            'ward': 'Ward 10',
            'area': 'Changunarayan',
            'street': 'Changunarayan Road',
            'landmark': 'Changunarayan Temple',
            'latitude': 27.7188,
            'longitude': 85.4154,
            'place_type': 'religious',
            'formatted_address': 'Changunarayan Road, Ward 10, Bhaktapur Metropolitan City, Bhaktapur, Bagmati Province, Nepal',
            'search_terms': ['changunarayan', 'temple', 'ward 10', 'bhaktapur'],
        },
    ],
}


def get_city_by_id(city_id: str | None) -> dict | None:
    if city_id is None:
        return None
    return CITY_SEED.get(city_id)


def _haversine_km(lat_a: float, lon_a: float, lat_b: float, lon_b: float) -> float:
    radius_km = 6371.0
    lat1 = math.radians(lat_a)
    lon1 = math.radians(lon_a)
    lat2 = math.radians(lat_b)
    lon2 = math.radians(lon_b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


def get_best_matching_address_for_coordinates(
    latitude: float,
    longitude: float,
    city_id: str | None = None,
    max_distance_km: float = 2.0,
) -> dict | None:
    if latitude is None or longitude is None:
        return None

    candidate_city_ids = [city_id] if city_id else list(CITY_ADDRESS_INDEX.keys())
    best_match = None
    best_distance = float('inf')

    for active_city_id in candidate_city_ids:
        for candidate in CITY_ADDRESS_INDEX.get(active_city_id, []):
            try:
                distance_km = _haversine_km(
                    float(latitude),
                    float(longitude),
                    float(candidate.get('latitude', 0.0)),
                    float(candidate.get('longitude', 0.0)),
                )
            except (TypeError, ValueError):
                continue

            if distance_km <= max_distance_km and distance_km < best_distance:
                best_match = dict(candidate)
                best_distance = distance_km

    if best_match is not None:
        best_match['distance_km'] = round(best_distance, 4)
        return best_match

    if city_id is not None:
        city_candidates = get_city_address_index(city_id)
        if city_candidates:
            ref = min(
                city_candidates,
                key=lambda item: _haversine_km(
                    float(latitude),
                    float(longitude),
                    float(item.get('latitude', 0.0)),
                    float(item.get('longitude', 0.0)),
                ),
            )
            ref = dict(ref)
            ref['distance_km'] = round(
                _haversine_km(
                    float(latitude),
                    float(longitude),
                    float(ref.get('latitude', 0.0)),
                    float(ref.get('longitude', 0.0)),
                ),
                4,
            )
            return ref

    return None


def get_default_city() -> dict:
    return KATHMANDU_CITY


def get_city_streets(city_id: str | None) -> list[str]:
    city = get_city_by_id(city_id)
    if city is None:
        return []
    return city.get('streets', [])


def get_city_address_index(city_id: str | None) -> list[dict]:
    if city_id is None:
        return []
    return [dict(item) for item in CITY_ADDRESS_INDEX.get(city_id, [])]


def get_address_by_id(city_id: str | None, address_id: str | None) -> dict | None:
    if city_id is None or address_id is None:
        return None
    for address in get_city_address_index(city_id):
        if address['id'] == address_id:
            return address
    return None


def search_city_addresses(city_id: str | None, query: str | None) -> list[dict]:
    addresses = get_city_address_index(city_id)
    if not addresses:
        return []

    normalized_query = re.sub(r'[^a-z0-9\s]', ' ', (query or '').lower()).strip()
    if not normalized_query:
        return addresses[:10]

    matches: list[tuple[float, dict]] = []
    for address in addresses:
        haystack = ' '.join([
            str(address.get('area', '')),
            str(address.get('street', '')),
            str(address.get('landmark', '')),
            str(address.get('municipality', '')),
            str(address.get('ward', '')),
            str(address.get('formatted_address', '')),
            *[str(item) for item in address.get('search_terms', [])],
        ]).lower()
        haystack = re.sub(r'[^a-z0-9\s]', ' ', haystack)
        if normalized_query in haystack:
            score = 1.0
            if haystack.startswith(normalized_query):
                score += 0.5
            if normalized_query.split()[0] in haystack:
                score += 0.2
            matches.append((score, dict(address)))

    matches.sort(key=lambda item: item[0], reverse=True)
    return [match for _, match in matches]


def get_default_city() -> dict:
    return KATHMANDU_CITY
