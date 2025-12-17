"""
Module for testing login functionality.

This module covers test cases for user login, including valid and invalid credentials.
"""

import pytest
from unittest.mock import Mock
from typing import Dict

# Fixtures
@pytest.fixture
def test_data() -> Dict[str, str]:
    """Returns test data for login."""
    return {
        "email": "test@example.com",
        "password": "password123"
    }

@pytest.fixture
def mock_login_service() -> Mock:
    """Returns a mock login service."""
    return Mock()

@pytest.fixture
def mock_dashboard() -> Mock:
    """Returns a mock dashboard."""
    return Mock()

# Test Cases
@pytest.mark.functional
@pytest.mark.critical
def test_valid_login_with_correct_credentials(test_data: Dict[str, str], mock_login_service: Mock, mock_dashboard: Mock) -> None:
    """
    Test valid login with correct credentials.

    This test validates that a user can login with valid email and password.
    """
    # Arrange
    mock_login_service.login.return_value = True
    mock_dashboard.redirect.return_value = None

    # Act
    result = login(test_data["email"], test_data["password"], mock_login_service, mock_dashboard)

    # Assert
    assert result is None, "Expected no error on valid login"
    mock_login_service.login.assert_called_once_with(test_data["email"], test_data["password"])
    mock_dashboard.redirect.assert_called_once()

def login(email: str, password: str, login_service: Mock, dashboard: Mock) -> None:
    """
    Simulates a login action.

    Args:
    - email (str): The user's email.
    - password (str): The user's password.
    - login_service (Mock): The login service.
    - dashboard (Mock): The dashboard.
    """
    if login_service.login(email, password):
        dashboard.redirect()
    else:
        raise ValueError("Invalid credentials")

def main() -> None:
    pass

if __name__ == "__main__":
    main()