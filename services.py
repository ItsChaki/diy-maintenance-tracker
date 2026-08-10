from typing import Optional
from database import get_connection

def add_service_record(
    vehicle_id: int,
    service_date: str,
    mileage: int,
    is_diy: bool,
    service_center: Optional[str] = None,
    total_cost: Optional[int] = None,
    notes: Optional[str] = None,
) -> int:
    """
    This function adds the service record to a existing vehicle. Service details are required.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO ServiceRecord (vehicleId, serviceDate, mileage, isDiy, serviceCenter, totalCost, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """ ,
        (vehicle_id, service_date, mileage, is_diy, service_center, total_cost, notes,),
    )
    serviceID = cursor.lastrowid
    conn.commit()
    conn.close()
    return serviceID


def get_service_record(record_id: int) -> Optional[tuple]:
    """
    pulls the service record of a given vehicle
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM ServiceRecord WHERE id = ?
        """,
        (record_id,)
    )
    
    serviceRecord = cursor.fetchone()
    conn.close()

    return serviceRecord

def list_services_for_vehicle(vehicle_id: int) -> list[tuple]:
    """
    fetches all services for a vehicle, newest first. WHERE vehicleId gets just the given records for a vehicle
    """
    #establish connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM ServiceRecord
        WHERE vehicleId = ?
        ORDER BY serviceDate DESC   
        """,
        (vehicle_id,)
    )
    services = cursor.fetchall()
    conn.close()

    return services

def delete_service_record(record_id: int) -> None:
    """
    Given record_id, service record is deleted. CASCADE takes care of service line items
    """
    conn = get_connection()
    cursor = conn.cursor()
    #deletes service record, CASCADE takes care of service line items
    cursor.execute(
        """
        DELETE FROM ServiceRecord WHERE id = ?  
        """,
        (record_id,)
    )
    conn.commit()
    conn.close()

def add_line_item(
    service_record_id: int,
    service_type: str,
    product_used: Optional[str] = None,
    quantity: int = 1,
    cost: Optional[int] = None,
    notes: Optional[str] = None,
) -> int:
    """
    Adds the details to a service record.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO ServiceLineItem (serviceRecordId, serviceType, productUsed, quantity, cost, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (service_record_id, service_type, product_used, quantity, cost, notes),
    )

    serviceID = cursor.lastrowid
    conn.commit()
    conn.close()
    return serviceID

def get_line_items(service_record_id: int) -> list[tuple]:
    """
    Retrieves the line items in a service record. 
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM ServiceLineItem
        WHERE serviceRecordId = ?
        ORDER BY id ASC
        """,
        (service_record_id,)
    )

    lineItems = cursor.fetchall()
    conn.close()

    return lineItems

def log_service_with_items(
    vehicle_id: int,
    service_date: str,
    mileage: int,
    is_diy: bool,
    items: list[dict],
    service_center: Optional[str] = None,
    total_cost: Optional[int] = None,
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
        cursor.execute( 
            """
            INSERT INTO ServiceRecord (vehicleId, serviceDate, mileage, isDiy, serviceCenter, totalCost, notes) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, 
            (vehicle_id, service_date, mileage, is_diy, service_center, total_cost, notes),
        )
        new_service_id = cursor.lastrowid

        #Insert each line item, referencing the parent
        for item in items:
            cursor.execute(
                """
                INSERT INTO ServiceLineItem
                    (serviceRecordId, serviceType, productUsed, quantity, cost, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    new_service_id,
                    item["serviceType"],
                    item.get("productUsed"),
                    item.get("quantity", 1),
                    item.get("cost"),
                    item.get("notes"),
                ),
            )

        conn.commit()  #ONLY commits if everything above succeeded
        return new_service_id

    except Exception:
        conn.rollback()  #undo everything if anything fails
        raise
    finally:
        conn.close()