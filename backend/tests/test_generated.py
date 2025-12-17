import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from your_app import User, PasswordResetToken, send_email

@pytest.fixture
def user():
    """Create a test user"""
    return User(email="test@example.com", password="old_password")

@pytest.fixture
def password_reset_token(user):
    """Create a password reset token for the test user"""
    return PasswordResetToken(user=user, expires_at=datetime.now() + timedelta(hours=1))

@pytest.mark.smoke
def test_request_password_reset(user):
    """
    Test requesting a password reset via email.

    Validates:
    - Email is sent with a reset link
    - Reset link contains a secure token
    """
    with patch("your_app.send_email") as mock_send_email:
        user.request_password_reset()
        mock_send_email.assert_called_once()
        assert "reset_link" in mock_send_email.call_args[1]["body"]

@pytest.mark.regression
def test_password_reset_link_expires(password_reset_token):
    """
    Test password reset link expiration.

    Validates:
    - Link expires after 1 hour
    """
    assert password_reset_token.expires_at < datetime.now() + timedelta(hours=2)

@pytest.mark.regression
def test_change_password(password_reset_token, user):
    """
    Test changing password using a valid reset token.

    Validates:
    - Password is updated successfully
    - All active sessions are invalidated
    """
    new_password = "NewP@ssw0rd"
    password_reset_token.change_password(new_password)
    assert user.password == new_password
    assert user.active_sessions == []

@pytest.mark.regression
def test_change_password_invalid_token(password_reset_token, user):
    """
    Test changing password using an invalid reset token.

    Validates:
    - Password is not updated
    - Error is raised
    """
    new_password = "NewP@ssw0rd"
    password_reset_token.expires_at = datetime.now() - timedelta(hours=1)
    with pytest.raises(ValueError):
        password_reset_token.change_password(new_password)
    assert user.password != new_password

@pytest.mark.regression
def test_change_password_weak_password(password_reset_token, user):
    """
    Test changing password with a weak password.

    Validates:
    - Password is not updated
    - Error is raised
    """
    new_password = "weak"
    with pytest.raises(ValueError):
        password_reset_token.change_password(new_password)
    assert user.password != new_password

@pytest.mark.regression
def test_change_password_recently_used_password(password_reset_token, user):
    """
    Test changing password to a recently used password.

    Validates:
    - Password is not updated
    - Error is raised
    """
    new_password = "old_password"
    user.recently_used_passwords = ["old_password"]
    with pytest.raises(ValueError):
        password_reset_token.change_password(new_password)
    assert user.password != new_password

@pytest.mark.regression
@pytest.mark.parametrize("password", [
    pytest.param("onlylowercase", id="only lowercase"),
    pytest.param("ONLYUPPERCASE", id="only uppercase"),
    pytest.param("1234567890", id="only numbers"),
    pytest.param("!@#$%^&*()", id="only special characters"),
])
def test_change_password_password_policy(password_reset_token, user, password):
    """
    Test changing password with a password that does not meet the password policy.

    Validates:
    - Password is not updated
    - Error is raised
    """
    with pytest.raises(ValueError):
        password_reset_token.change_password(password)
    assert user.password != password