from sqlalchemy import text


def test_authenticate(auth_service, test_db_session):
    # Arrange
    test_db_session.execute(
        text("""
        INSERT INTO employees (surname, name, patronymic, position, phone, login, password)
        VALUES ('Ivanov', 'Ivan', 'Ivanovich', 'Admin', '1234567890', 'admin', 'password')
        """)
    )
    test_db_session.commit()

    # Act
    user = auth_service.authenticate("admin", "password")

    # Assert
    assert user is not None
    assert user.login == "admin"
