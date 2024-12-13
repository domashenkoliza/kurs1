from datetime import date

def test_create_repair(repair_service, test_db_session):
    # Act
    repair = repair_service.create_repair(
        shoe_id=1, client_id=1, employee_id=1, status="In Progress", 
        received_date=date(2024, 1, 1), due_date=date(2024, 1, 10)
    )

    # Assert
    assert repair.id is not None
    assert repair.status == "In Progress"

def test_get_repairs(repair_service, test_db_session):
    # Arrange
    repair_service.create_repair(
        shoe_id=1, client_id=1, employee_id=1, status="In Progress", 
        received_date=date(2024, 1, 1), due_date=date(2024, 1, 10)
    )

    # Act
    repairs = repair_service.get_repairs()

    # Assert
    assert len(repairs) == 1

def test_delete_repair(repair_service, test_db_session):
    # Arrange
    repair = repair_service.create_repair(
        shoe_id=1, client_id=1, employee_id=1, status="In Progress", 
        received_date=date(2024, 1, 1), due_date=date(2024, 1, 10)
    )

    # Act
    repair_service.delete_repair(repair.id)
    repairs = repair_service.get_repairs()

    # Assert
    assert len(repairs) == 0
