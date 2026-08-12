import pytest
import sqlite3
import database
from vehicles import add_vehicle, delete_vehicle
from services import (
    add_service_record, get_service_record, list_services_for_vehicle,
    delete_service_record, add_line_item, get_line_items,
    log_service_with_items,
)

@pytest.fixture
def test_db(tmp_path):
    """
    Sets up a fresh temporary database for each test.
    """
    db_path = tmp_path / "test_garage.db"

    #Apply schema to the temp database
    conn = sqlite3.connect(str(db_path))
    with open("schema.sql") as f:
        conn.executescript(f.read())
    conn.close()

    #Point the database module at our temp file for this test
    original_path = database.DB_PATH
    database.DB_PATH = str(db_path)

    yield  #the test runs here

    #Restore the original path after the test
    database.DB_PATH = original_path


@pytest.fixture
def vehicle_id(test_db):
    """A vehicle already in the temp db, so service tests have a valid FK target."""
    return add_vehicle("1HGBH41JXMN109186", 2020, "Toyota", "Corolla")

def test_add_service_record(vehicle_id):
    """Adding a service record returns its id and the row is retrievable."""
    new_id = add_service_record(
        vehicle_id=vehicle_id,
        service_date="2026-05-26",
        mileage=50000,
        is_diy=True,
        total_cost=4500,
    )
    assert new_id == 1

    record = get_service_record(new_id)
    assert record is not None
    assert record[1] == vehicle_id   # vehicleId column
    assert record[3] == 50000        # mileage


def test_log_service_with_items_rolls_back(vehicle_id):
    """A malformed item aborts the whole transaction — no orphan header survives."""
    bad_items = [
        {"serviceType": "Oil Change", "cost": 4500},
        {"productUsed": "Fram PH7317", "cost": 1200},  # no serviceType
    ]

    with pytest.raises(KeyError):
        log_service_with_items(
            vehicle_id=vehicle_id,
            service_date="2026-05-26",
            mileage=50000,
            is_diy=True,
            items=bad_items,
        )

    # the parent insert already ran before the failure — prove it didn't stick
    assert list_services_for_vehicle(vehicle_id) == []