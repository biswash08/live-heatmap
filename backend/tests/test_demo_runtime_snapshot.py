from infrastructure.simulation.demo_runner import build_demo_runtime_snapshot


def test_demo_runtime_snapshot_produces_heatmap_and_nearby_drivers():
    snapshot = build_demo_runtime_snapshot()

    assert snapshot['city_id'] == 'ktm'
    assert snapshot['heatmap']['total_driver_count'] >= 2
    assert 'nearby_drivers' in snapshot
    assert len(snapshot['nearby_drivers']) >= 1
    assert snapshot['surge']['city_id'] == 'ktm'
