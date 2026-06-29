#test file for vehicles.py
import sqlite3
import pytest
import database
from vehicles import add_vehicle, get_vehicle, list_vehicles, update_vehicle_nickname

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


def test_add_vehicle(test_db):
    """Adding a vehicle returns its new id and the row is retrievable."""
    new_id = add_vehicle(
        vin="1HGBH41JXMN109186",
        year=2020,
        make="Toyota",
        model="Corolla",
        nickname="Daily Driver",
    )

    assert new_id == 1  #first row, auto-incremented from 1

    vehicle = get_vehicle(new_id)
    assert vehicle is not None
    assert vehicle[1] == "1HGBH41JXMN109186"  #vin
    assert vehicle[3] == "Toyota"               #make
    assert vehicle[7] == "Daily Driver"         #nickname


def test_get_vehicle_not_found(test_db):
    """
    testing to see we get a result of None
    """
    result = get_vehicle(999)
    assert result == None


def test_list_vehicles(test_db):
    """
    Adds vehicles to the database, make sure lengths match
    """
    #add 3 vehicles
    add_vehicle(
        vin="1HGBH41JXMN109186",
        year=2020,
        make="Toyota",
        model="Corolla",
        nickname="Girlfriend's Car",
    )
    add_vehicle(
        vin="1HGBH41JXMN155387",
        year=2013,
        make="Nissan",
        model="Altima",
        nickname="Helltima",
    )
    add_vehicle(
        vin="1HGBH41JXMN482950",
        year=2017,
        make="Nissan",
        model="Maxima",
        nickname="Dad's car",
    )

    #result comes back as list of tuples
    testList = list_vehicles()
    assert len(testList) == 3


def test_update_vehicle_name(test_db):
    """
    Add a vehicle to the test_db, update nickname, verify nickname has been changed
    """
    #get vehicle id
    new_id = add_vehicle(
        vin="1HGBH41JXMN155387",
        year=2013,
        make="Nissan",
        model="Altima",
        nickname="Helltima",
    )
    #update name and then get row given id
    update_vehicle_nickname(new_id, "Chaki's Car")
    test = get_vehicle(new_id)
    assert test[7] == "Chaki's Car"



def test_duplicate_vin_raises(test_db):
    """The UNIQUE constraint on VIN should prevent duplicate inserts."""
    add_vehicle("1HGBH41JXMN109186", 2020, "Toyota", "Corolla")
    with pytest.raises(sqlite3.IntegrityError):
        add_vehicle("1HGBH41JXMN109186", 2021, "Honda", "Civic")