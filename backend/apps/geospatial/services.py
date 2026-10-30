"""Geospatial utilities built on Uber H3."""

from __future__ import annotations

import h3


def get_h3_cell(latitude: float, longitude: float, resolution: int = 8) -> str:
    return h3.latlng_to_cell(float(latitude), float(longitude), resolution)


def get_neighbouring_cells(h3_cell: str, k: int = 1) -> list[str]:
    return h3.grid_disk(h3_cell, k)


def get_cell_boundary(h3_cell: str) -> list[list[float]]:
    boundary = h3.cell_to_boundary(h3_cell)
    return [[float(lat), float(lng)] for lat, lng in boundary]


def get_cell_center(h3_cell: str) -> tuple[float, float]:
    lat, lng = h3.cell_to_latlng(h3_cell)
    return float(lat), float(lng)


def get_cells_in_radius(latitude: float, longitude: float, radius_km: float, resolution: int = 8) -> list[str]:
    center_hex = get_h3_cell(latitude, longitude, resolution)
    return h3.grid_disk(center_hex, int(radius_km))
