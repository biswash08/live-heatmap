"""Dynamic surge pricing logic."""


def compute_surge_multiplier(available_drivers: int, active_requests: int, target_ratio: float = 0.25) -> float:
    demand_ratio = active_requests / max(available_drivers, 1)
    multiplier = 1.0 + max(0.0, demand_ratio - target_ratio)
    return min(max(multiplier, 1.0), 5.0)
