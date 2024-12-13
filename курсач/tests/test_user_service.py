def test_add_client(user_service, test_db_session):
    # Act
    client = user_service.add_client(
        surname="Ivanov", name="Ivan", patronymic="Ivanovich", phone="1234567890"
    )

    # Assert
    assert client.id is not None
    assert client.name == "Ivan"

def test_get_clients(user_service, test_db_session):
    # Arrange
    user_service.add_client(surname="Ivanov", name="Ivan", patronymic="Ivanovich", phone="1234567890")

    # Act
    clients = user_service.get_clients()

    # Assert
    assert len(clients) == 1

def test_delete_client(user_service, test_db_session):
    # Arrange
    client = user_service.add_client(surname="Ivanov", name="Ivan", patronymic="Ivanovich", phone="1234567890")

    # Act
    user_service.delete_client(client.id)
    clients = user_service.get_clients()

    # Assert
    assert len(clients) == 0
