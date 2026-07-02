import sqlite3
from typing import Optional
from database import get_connection

def log_service_with_items(vehicle_id: int,
    service_date: str,
    mileage: int,
    is_diy: bool,
    items: list[dict],
    service_center: Optional[str] = None,
    notes: Optional[str] = None,
) -> int:
    """
    """

def add_service_record(vehicle_id, service_date, mileage, is_diy, 
                       service_center=None, total_cost=None, notes=None)
    """
    """