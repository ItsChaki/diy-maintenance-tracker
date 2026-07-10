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
    Creates a ServiceRecord AND inserts all its line items in a single transaction.
    If any line item fails, the entire operation rolls back.

    items is a list of dicts like:
        [{"serviceType": "Oil Change", "productUsed": "Valvoline 5W-30", "quantity": 1, "cost": 4500}, ...]

    Returns the new service_record id.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        #Insert the ServiceRecord (parent)
        cursor.execute("INSERT INTO ServiceRecord (...) VALUES (...)", (...))
        new_service_id = cursor.lastrowid

        #Insert each line item, referencing the parent
        for item in items:
            cursor.execute("INSERT INTO ServiceLineItem (...) VALUES (...)", (...))

        conn.commit()  #ONLY commits if everything above succeeded
        return new_service_id

    except sqlite3.Error:
        conn.rollback()  #undo everything if anything fails
        raise
    finally:
        conn.close()

def add_service_record(vehicle_id, service_date, mileage, is_diy, 
                       service_center=None, total_cost=None, notes=None):
    """
    This function adds the service record to a existing vehicle. Service details are required
    """
    conn = get_connection()


def get_service_record(record_id):
    """
    pulls the service record of a given vehicle
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
    