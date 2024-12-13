def test_add_service(service_journal_service, test_db_session):
    # Act
    service = service_journal_service.add_service(name="Repair", cost=1000.0)

    # Assert
    assert service.id is not None
    assert service.name == "Repair"

def test_get_services(service_journal_service, test_db_session):
    # Arrange
    service_journal_service.add_service(name="Repair", cost=1000.0)

    # Act
    services = service_journal_service.get_services()

    # Assert
    assert len(services) == 1

def test_delete_service(service_journal_service, test_db_session):
    # Arrange
    service = service_journal_service.add_service(name="Repair", cost=1000.0)

    # Act
    service_journal_service.delete_service(service.id)
    services = service_journal_service.get_services()

    # Assert
    assert len(services) == 0
