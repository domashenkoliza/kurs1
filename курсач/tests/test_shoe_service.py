def test_add_shoe(shoe_service, test_db_session):
    # Act
    shoe = shoe_service.add_shoe(service_id=1, client_id=1, size="42", name="Boots")

    # Assert
    assert shoe.id is not None
    assert shoe.name == "Boots"

def test_get_shoes(shoe_service, test_db_session):
    # Arrange
    shoe_service.add_shoe(service_id=1, client_id=1, size="42", name="Boots")

    # Act
    shoes = shoe_service.get_shoes()

    # Assert
    assert len(shoes) == 1

def test_delete_shoe(shoe_service, test_db_session):
    # Arrange
    shoe = shoe_service.add_shoe(service_id=1, client_id=1, size="42", name="Boots")

    # Act
    shoe_service.delete_shoe(shoe.id)
    shoes = shoe_service.get_shoes()

    # Assert
    assert len(shoes) == 0
