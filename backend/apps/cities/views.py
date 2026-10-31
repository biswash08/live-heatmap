from rest_framework.response import Response
from rest_framework.views import APIView

from .seed import CITY_SEED, get_city_address_index, get_city_by_id, search_city_addresses


class CityDirectoryView(APIView):
    def get(self, request, *args, **kwargs):
        cities = []
        for city_id, city in sorted(CITY_SEED.items()):
            city_payload = {
                'id': city.get('id'),
                'name': city.get('name'),
                'slug': city.get('slug'),
                'province': city.get('province', 'Nepal'),
                'district': city.get('district'),
                'municipality': city.get('municipality', city.get('name')),
                'lat': city.get('lat'),
                'lng': city.get('lng'),
                'address_count': len(get_city_address_index(city_id)),
            }
            cities.append(city_payload)

        return Response({'count': len(cities), 'cities': cities})


class CityAddressSearchView(APIView):
    def get(self, request, city_id, *args, **kwargs):
        city = get_city_by_id(city_id)
        if city is None:
            return Response({'detail': 'City not found.'}, status=404)

        query = (request.query_params.get('query') or '').strip()
        addresses = search_city_addresses(city_id, query) if query else get_city_address_index(city_id)

        payload = {
            'city_id': city_id,
            'city_name': city.get('name'),
            'province': city.get('province', 'Nepal'),
            'district': city.get('district'),
            'municipality': city.get('municipality', city.get('name')),
            'count': len(addresses),
            'addresses': addresses,
        }
        return Response(payload)
