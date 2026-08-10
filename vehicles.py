import sqlite3
from typing import Optional
from database import get_connection

#CRUD FUNCTIONS
def add_vehicle(vin: str, year: int, make: str, model: str, 
    trim: Optional[str] = None, engineSize: Optional[str] = None, 
    nickname: Optional[str] = None,
    ) -> int:
    """
    Inserting a new vehicle into the database.
    Returns the id of the newly inserted vehicle.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Vehicle (vin, year, make, model, trim, engineSize, nickname)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (vin, year, make, model, trim, engineSize, nickname),
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return new_id


def get_vehicle(vehicle_id: int) -> Optional[tuple]:
    """
    Given vehicle_id, returns a tuple of row's values. None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM Vehicle WHERE id = ?
        """,
        (vehicle_id,)
    )
    
    vehicle = cursor.fetchone()
    conn.close()

    return vehicle


def list_vehicles() -> list[tuple]:
    """
    Returns all current vehicles as tuples
    """    

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM Vehicle
        """)
    vehicles = cursor.fetchall()
    conn.close()

    return vehicles



def update_vehicle_nickname(vehicle_id: int, nickname: str) -> None:
    """
    Given vehicle_id, updates the nickname of given vehicle
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Vehicle SET nickname = ? WHERE id = ?
        """,
        (nickname, vehicle_id)
    )

    conn.commit()
    conn.close()


def delete_vehicle(vehicle_id: int) -> None:
    """
    Deletes a vehicle AND all its service records AND all their line items
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM Vehicle WHERE id = ?
        """,
        (vehicle_id,)
    )

    conn.commit()
    conn.close()

