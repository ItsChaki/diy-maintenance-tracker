import sqlite3
import pytest
import database
from vehicles import add_vehicle, delete_vehicle
from services import (
    add_service_record, get_service_record, list_services_for_vehicle,
    delete_service_record, add_line_item, get_line_items,
    log_service_with_items,
)

@pytest.fixture
def test_db(tmp_path):
    # ... identical to test_vehicles.py ...
    ...

@pytest.fixture
def vehicle_id(test_db):
    """A vehicle already in the temp db, so service tests have a valid FK target."""
    return add_vehicle("1HGBH41JXMN109186", 2020, "Toyota", "Corolla")