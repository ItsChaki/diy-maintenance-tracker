#test file for vehicles.py
import sqlite3
import pytest
import database
from vehicles import add_vehicle, get_vehicle


def test_duplicate_vin_raises(test_db):
    """The UNIQUE constraint on VIN should prevent duplicate inserts."""
    add_vehicle("1HGBH41JXMN109186", 2020, "Toyota", "Corolla")
    with pytest.raises(sqlite3.IntegrityError):
        add_vehicle("1HGBH41JXMN109186", 2021, "Honda", "Civic")