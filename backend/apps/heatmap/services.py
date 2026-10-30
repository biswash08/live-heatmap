"""Heatmap service layer."""

from __future__ import annotations

from infrastructure.redis.state_store import DriverStateStore


def classify_density(driver_count: int) -> str:
    if driver_count == 0:
        return 'empty'
    if 1 <= driver_count <= 3:
        return 'very_low'
    if 4 <= driver_count <= 10:
        return 'low'
    if 11 <= driver_count <= 25:
        return 'medium'
    if 26 <= driver_count <= 50:
        return 'high'
    return 'very_high'


def build_heatmap_response(city_id: str, north: float, south: float, east: float, west: float, resolution: int = 8) -> dict:
    store = DriverStateStore.shared()
    cells = []
    for state in store.driver_states.values():
        if state.city_id != city_id:
            continue
        lat = state.latitude
        lon = state.longitude
        if not (south <= lat <= north and west <= lon <= east):
            continue
        cell_key = f'cell:{city_id}:{state.current_h3_cell}'
        count = store.cell_counts.get(cell_key, 0)
        cells.append({
            'h3_index': state.current_h3_cell,
            'driver_count': count,
            'density': classify_density(count),
            'boundary': [],
        })
    return {'city_id': city_id, 'updated_at': '2026-10-31T01:00:00Z', 'cells': cells}
