def test_add_employee(employee_service, test_db_session):
    # Act
    employee = employee_service.add_employee(
        surname="Petrov", name="Petr", patronymic="Petrovich",
        position="Master", phone="1234567890", login="petrov", password="password"
    )

    # Assert
    assert employee.id is not None
    assert employee.name == "Petr"

def test_get_employees(employee_service, test_db_session):
    # Arrange
    employee_service.add_employee(
        surname="Petrov", name="Petr", patronymic="Petrovich",
        position="Master", phone="1234567890", login="petrov", password="password"
    )

    # Act
    employees = employee_service.get_employees()

    # Assert
    assert len(employees) == 1

def test_delete_employee(employee_service, test_db_session):
    # Arrange
    employee = employee_service.add_employee(
        surname="Petrov", name="Petr", patronymic="Petrovich",
        position="Master", phone="1234567890", login="petrov", password="password"
    )

    # Act
    employee_service.delete_employee(employee.id)
    employees = employee_service.get_employees()

    # Assert
    assert len(employees) == 0
