from datetime import date

def test_create_order(order_service, test_db_session):
    # Act
    order = order_service.create_order(
        repair_id=1, employee_id=1, client_id=1, total_cost=1000.0, order_date=date(2024, 1, 1)
    )

    # Assert
    assert order.id is not None
    assert order.total_cost == 1000.0

def test_get_orders(order_service, test_db_session):
    # Arrange
    order_service.create_order(
        repair_id=1, employee_id=1, client_id=1, total_cost=1000.0, order_date=date(2024, 1, 1)
    )

    # Act
    orders = order_service.get_orders()

    # Assert
    assert len(orders) == 1

def test_delete_order(order_service, test_db_session):
    # Arrange
    order = order_service.create_order(
        repair_id=1, employee_id=1, client_id=1, total_cost=1000.0, order_date=date(2024, 1, 1)
    )

    # Act
    order_service.delete_order(order.id)
    orders = order_service.get_orders()

    # Assert
    assert len(orders) == 0
