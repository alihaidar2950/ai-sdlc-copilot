# AI SDLC Co-Pilot — Prompt Engineering Guide

**Version:** 1.0
**Last Updated:** 2025-12-10

This document contains all LLM prompt templates used in AI SDLC Co-Pilot. These prompts are designed to work with multiple LLM providers (Gemini, Groq, OpenAI) and produce consistent, structured outputs.

---

## Table of Contents

1. [Prompt Design Principles](#prompt-design-principles)
2. [Test Case Generation](#1-test-case-generation)
3. [PyTest Skeleton Generation](#2-pytest-skeleton-generation)
4. [PR Review](#3-pr-review)
5. [Defect/Issue Creation](#4-defectissue-creation)
6. [Output Schemas](#output-schemas)
7. [Provider-Specific Notes](#provider-specific-notes)
8. [Prompt Versioning](#prompt-versioning)

---

## Prompt Design Principles

### Structure
All prompts follow this pattern:
```
[SYSTEM] - Role and constraints
[CONTEXT] - Background information
[TASK] - What to do
[FORMAT] - Expected output format
[EXAMPLES] - Few-shot examples (optional)
[INPUT] - User's actual input
```

### Best Practices
1. **Be explicit** — State exactly what you want
2. **Use JSON output** — Structured data is easier to parse
3. **Include examples** — Few-shot learning improves consistency
4. **Set constraints** — Prevent hallucination with guardrails
5. **Version prompts** — Track changes for debugging

---

## 1. Test Case Generation

### Purpose
Convert a requirement (user story, feature brief, API spec) into structured test cases.

### Prompt Template

```
SYSTEM:
You are a senior QA engineer with 10+ years of experience in test design. Your specialty is creating comprehensive, well-structured test cases from requirements. You think systematically about edge cases, boundary conditions, and failure scenarios.

CONTEXT:
You are helping a development team create test cases for their software. The test cases should be:
- Clear and unambiguous
- Testable and measurable
- Cover positive, negative, and edge cases
- Follow best practices for test design

TASK:
Analyze the following requirement and generate comprehensive test cases.

For each test case, provide:
1. A unique ID (TC_XXX format)
2. A descriptive title
3. Priority (High/Medium/Low)
4. Type (Positive/Negative/Edge/Boundary)
5. Preconditions (what must be true before the test)
6. Test steps (numbered, actionable steps)
7. Expected results (specific, measurable outcomes)
8. Postconditions (system state after test)

OUTPUT FORMAT:
Respond with valid JSON only. No markdown, no explanation, just the JSON object.

{
  "requirement_summary": "Brief summary of the requirement",
  "test_cases": [
    {
      "id": "TC_001",
      "title": "Descriptive test case title",
      "priority": "High|Medium|Low",
      "type": "Positive|Negative|Edge|Boundary",
      "preconditions": ["Precondition 1", "Precondition 2"],
      "steps": [
        {"step": 1, "action": "Do something", "data": "test data if any"},
        {"step": 2, "action": "Do something else", "data": null}
      ],
      "expected_results": ["Expected result 1", "Expected result 2"],
      "postconditions": ["System state after test"]
    }
  ],
  "coverage_notes": "Any gaps or areas needing clarification"
}

REQUIREMENT:
{requirement_text}
```

### Example Input

```
As a user, I want to reset my password via email so that I can regain access to my account if I forget my credentials.

Acceptance Criteria:
- User clicks "Forgot Password" link on login page
- User enters their registered email address
- System sends password reset email within 2 minutes
- Email contains a unique reset link
- Reset link expires after 24 hours
- User can set a new password that meets complexity requirements
- Password must be at least 8 characters with 1 uppercase, 1 lowercase, 1 number
- User cannot reuse last 5 passwords
```

### Example Output

```json
{
  "requirement_summary": "Password reset functionality via email with secure link and password complexity requirements",
  "test_cases": [
    {
      "id": "TC_001",
      "title": "Successful password reset with valid email",
      "priority": "High",
      "type": "Positive",
      "preconditions": [
        "User has a registered account with email user@example.com",
        "User is on the login page",
        "Email service is operational"
      ],
      "steps": [
        {"step": 1, "action": "Click 'Forgot Password' link", "data": null},
        {"step": 2, "action": "Enter registered email address", "data": "user@example.com"},
        {"step": 3, "action": "Click 'Send Reset Link' button", "data": null},
        {"step": 4, "action": "Check email inbox", "data": null},
        {"step": 5, "action": "Click reset link in email", "data": null},
        {"step": 6, "action": "Enter new password", "data": "NewPass123"},
        {"step": 7, "action": "Confirm new password", "data": "NewPass123"},
        {"step": 8, "action": "Click 'Reset Password' button", "data": null}
      ],
      "expected_results": [
        "Reset email received within 2 minutes",
        "Email contains unique reset link",
        "Password successfully changed",
        "User can login with new password",
        "Confirmation message displayed"
      ],
      "postconditions": [
        "User password is updated in database",
        "Reset link is invalidated",
        "User session is created after login"
      ]
    },
    {
      "id": "TC_002",
      "title": "Password reset with unregistered email",
      "priority": "High",
      "type": "Negative",
      "preconditions": [
        "Email notregistered@example.com is not in the system",
        "User is on the forgot password page"
      ],
      "steps": [
        {"step": 1, "action": "Enter unregistered email", "data": "notregistered@example.com"},
        {"step": 2, "action": "Click 'Send Reset Link' button", "data": null}
      ],
      "expected_results": [
        "Generic message displayed (no indication if email exists for security)",
        "No email is sent",
        "No error reveals email existence"
      ],
      "postconditions": [
        "No password reset token created"
      ]
    },
    {
      "id": "TC_003",
      "title": "Reset link expires after 24 hours",
      "priority": "High",
      "type": "Boundary",
      "preconditions": [
        "User has requested password reset",
        "Reset link was generated 24+ hours ago"
      ],
      "steps": [
        {"step": 1, "action": "Click expired reset link from email", "data": null}
      ],
      "expected_results": [
        "Error message: 'Reset link has expired'",
        "User is prompted to request a new reset link",
        "Password is not changed"
      ],
      "postconditions": [
        "Expired token remains invalidated"
      ]
    },
    {
      "id": "TC_004",
      "title": "Password complexity - missing uppercase",
      "priority": "Medium",
      "type": "Negative",
      "preconditions": [
        "User is on the password reset page with valid token"
      ],
      "steps": [
        {"step": 1, "action": "Enter password without uppercase", "data": "newpass123"},
        {"step": 2, "action": "Confirm password", "data": "newpass123"},
        {"step": 3, "action": "Click 'Reset Password'", "data": null}
      ],
      "expected_results": [
        "Validation error displayed",
        "Message indicates uppercase letter required",
        "Password is not changed"
      ],
      "postconditions": [
        "Original password unchanged"
      ]
    },
    {
      "id": "TC_005",
      "title": "Cannot reuse recent password",
      "priority": "Medium",
      "type": "Negative",
      "preconditions": [
        "User's password history contains: Pass1, Pass2, Pass3, Pass4, Pass5",
        "User is on password reset page with valid token"
      ],
      "steps": [
        {"step": 1, "action": "Enter previously used password", "data": "Pass3"},
        {"step": 2, "action": "Confirm password", "data": "Pass3"},
        {"step": 3, "action": "Click 'Reset Password'", "data": null}
      ],
      "expected_results": [
        "Error: 'Cannot reuse recent passwords'",
        "Password is not changed"
      ],
      "postconditions": [
        "Password history unchanged"
      ]
    },
    {
      "id": "TC_006",
      "title": "Reset link can only be used once",
      "priority": "High",
      "type": "Edge",
      "preconditions": [
        "User has successfully reset password using a link"
      ],
      "steps": [
        {"step": 1, "action": "Click the same reset link again", "data": null}
      ],
      "expected_results": [
        "Error: 'This link has already been used'",
        "User cannot reset password again with same link"
      ],
      "postconditions": [
        "Token remains invalidated"
      ]
    }
  ],
  "coverage_notes": "Additional tests needed for: email delivery failures, rate limiting on reset requests, concurrent reset attempts, SQL injection in email field"
}
```

---

## 2. PyTest Skeleton Generation

### Purpose
Convert test case JSON into executable PyTest code skeleton.

### Prompt Template

```
SYSTEM:
You are a senior Python developer specializing in test automation with PyTest. You write clean, maintainable, well-documented test code following PEP 8 and PyTest best practices.

CONTEXT:
You are generating PyTest test skeletons from structured test cases. The code should:
- Use PyTest fixtures and markers appropriately
- Include clear docstrings
- Have placeholder assertions with TODO comments
- Be ready for implementation by a developer
- Follow AAA pattern (Arrange, Act, Assert)

TASK:
Generate a PyTest test file from the following test cases JSON.

Requirements:
1. Create a test class named Test{FeatureName}
2. Each test case becomes a test method
3. Use @pytest.mark.parametrize where appropriate
4. Include fixtures for common setup
5. Add TODO comments where implementation is needed
6. Include type hints

OUTPUT FORMAT:
Respond with valid Python code only. No markdown code blocks, no explanation.

TEST CASES JSON:
{test_cases_json}
```

### Example Output

```python
"""
Test Suite: Password Reset Functionality
Generated by AI SDLC Co-Pilot
Date: 2025-12-10

This module contains test cases for the password reset feature.
"""

import pytest
from datetime import datetime, timedelta
from typing import Generator
from unittest.mock import Mock, patch

# TODO: Import your actual modules
# from app.auth import PasswordResetService
# from app.models import User
# from app.email import EmailService


class TestPasswordReset:
    """Test suite for password reset functionality."""

    @pytest.fixture
    def registered_user(self) -> dict:
        """Fixture: Create a registered user for testing."""
        # TODO: Replace with actual user creation
        return {
            "id": "user-123",
            "email": "user@example.com",
            "password_hash": "hashed_password",
            "password_history": []
        }

    @pytest.fixture
    def email_service(self) -> Mock:
        """Fixture: Mock email service."""
        # TODO: Replace with actual email service mock
        return Mock()

    @pytest.fixture
    def password_reset_service(self, email_service: Mock) -> Mock:
        """Fixture: Password reset service instance."""
        # TODO: Replace with actual service instantiation
        return Mock()

    @pytest.mark.priority_high
    @pytest.mark.positive
    def test_tc_001_successful_password_reset_with_valid_email(
        self,
        registered_user: dict,
        password_reset_service: Mock,
        email_service: Mock
    ) -> None:
        """
        TC_001: Successful password reset with valid email
        
        Preconditions:
            - User has a registered account with email user@example.com
            - User is on the login page
            - Email service is operational
        
        Expected Results:
            - Reset email received within 2 minutes
            - Email contains unique reset link
            - Password successfully changed
            - User can login with new password
            - Confirmation message displayed
        """
        # Arrange
        email = "user@example.com"
        new_password = "NewPass123"
        
        # TODO: Set up test data and mocks
        # password_reset_service.request_reset.return_value = "reset-token-123"
        
        # Act
        # Step 1: Request password reset
        # TODO: reset_token = password_reset_service.request_reset(email)
        
        # Step 2: Verify email was sent
        # TODO: email_service.send_reset_email.assert_called_once()
        
        # Step 3: Reset password with token
        # TODO: result = password_reset_service.reset_password(reset_token, new_password)
        
        # Assert
        # TODO: Implement actual assertions
        # assert result.success is True
        # assert user can login with new_password
        pytest.skip("TODO: Implement test")

    @pytest.mark.priority_high
    @pytest.mark.negative
    def test_tc_002_password_reset_with_unregistered_email(
        self,
        password_reset_service: Mock
    ) -> None:
        """
        TC_002: Password reset with unregistered email
        
        Preconditions:
            - Email notregistered@example.com is not in the system
            - User is on the forgot password page
        
        Expected Results:
            - Generic message displayed (no indication if email exists for security)
            - No email is sent
            - No error reveals email existence
        """
        # Arrange
        unregistered_email = "notregistered@example.com"
        
        # Act
        # TODO: result = password_reset_service.request_reset(unregistered_email)
        
        # Assert
        # TODO: Verify generic response (security - don't reveal if email exists)
        # assert result.message == "If this email is registered, you will receive a reset link"
        # assert email_service.send_reset_email.not_called()
        pytest.skip("TODO: Implement test")

    @pytest.mark.priority_high
    @pytest.mark.boundary
    def test_tc_003_reset_link_expires_after_24_hours(
        self,
        registered_user: dict,
        password_reset_service: Mock
    ) -> None:
        """
        TC_003: Reset link expires after 24 hours
        
        Preconditions:
            - User has requested password reset
            - Reset link was generated 24+ hours ago
        
        Expected Results:
            - Error message: 'Reset link has expired'
            - User is prompted to request a new reset link
            - Password is not changed
        """
        # Arrange
        expired_token = "expired-token-123"
        new_password = "NewPass123"
        
        # TODO: Mock token creation time to be > 24 hours ago
        # with patch('app.auth.get_token_created_at') as mock_time:
        #     mock_time.return_value = datetime.now() - timedelta(hours=25)
        
        # Act
        # TODO: result = password_reset_service.reset_password(expired_token, new_password)
        
        # Assert
        # TODO: assert result.success is False
        # TODO: assert "expired" in result.error.lower()
        pytest.skip("TODO: Implement test")

    @pytest.mark.priority_medium
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_password,expected_error", [
        ("newpass123", "uppercase letter required"),
        ("NEWPASS123", "lowercase letter required"),
        ("NewPassABC", "number required"),
        ("New1", "at least 8 characters"),
    ])
    def test_tc_004_password_complexity_validation(
        self,
        registered_user: dict,
        password_reset_service: Mock,
        invalid_password: str,
        expected_error: str
    ) -> None:
        """
        TC_004: Password complexity validation
        
        Tests various password complexity requirements:
        - At least 8 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 number
        """
        # Arrange
        valid_token = "valid-token-123"
        
        # Act
        # TODO: result = password_reset_service.reset_password(valid_token, invalid_password)
        
        # Assert
        # TODO: assert result.success is False
        # TODO: assert expected_error in result.error.lower()
        pytest.skip("TODO: Implement test")

    @pytest.mark.priority_medium
    @pytest.mark.negative
    def test_tc_005_cannot_reuse_recent_password(
        self,
        registered_user: dict,
        password_reset_service: Mock
    ) -> None:
        """
        TC_005: Cannot reuse recent password
        
        Preconditions:
            - User's password history contains: Pass1, Pass2, Pass3, Pass4, Pass5
            - User is on password reset page with valid token
        
        Expected Results:
            - Error: 'Cannot reuse recent passwords'
            - Password is not changed
        """
        # Arrange
        valid_token = "valid-token-123"
        previously_used_password = "Pass3"
        
        # TODO: Set up user with password history
        # registered_user["password_history"] = ["Pass1", "Pass2", "Pass3", "Pass4", "Pass5"]
        
        # Act
        # TODO: result = password_reset_service.reset_password(valid_token, previously_used_password)
        
        # Assert
        # TODO: assert result.success is False
        # TODO: assert "reuse" in result.error.lower()
        pytest.skip("TODO: Implement test")

    @pytest.mark.priority_high
    @pytest.mark.edge
    def test_tc_006_reset_link_can_only_be_used_once(
        self,
        registered_user: dict,
        password_reset_service: Mock
    ) -> None:
        """
        TC_006: Reset link can only be used once
        
        Preconditions:
            - User has successfully reset password using a link
        
        Expected Results:
            - Error: 'This link has already been used'
            - User cannot reset password again with same link
        """
        # Arrange
        used_token = "already-used-token-123"
        new_password = "AnotherPass123"
        
        # TODO: Mock that this token was already used
        # password_reset_service.is_token_used.return_value = True
        
        # Act
        # TODO: result = password_reset_service.reset_password(used_token, new_password)
        
        # Assert
        # TODO: assert result.success is False
        # TODO: assert "already been used" in result.error.lower()
        pytest.skip("TODO: Implement test")


# Run with: pytest test_password_reset.py -v
```

---

## 3. PR Review

### Purpose
Analyze a code diff and provide actionable review comments.

### Prompt Template

```
SYSTEM:
You are a senior software engineer conducting a thorough code review. You have expertise in security, performance, maintainability, and best practices. Your reviews are constructive, specific, and actionable.

CONTEXT:
You are reviewing a pull request. Your review should:
- Focus on bugs, security issues, and performance problems
- Suggest improvements for readability and maintainability
- Be respectful and constructive
- Provide specific line references when possible
- Include code suggestions where helpful

TASK:
Review the following code diff and provide feedback.

For each issue found, provide:
1. Severity (Critical/High/Medium/Low/Info)
2. Category (Bug/Security/Performance/Style/Maintainability)
3. File and line number
4. Description of the issue
5. Suggested fix (with code if applicable)
6. Confidence score (0-100%)

OUTPUT FORMAT:
Respond with valid JSON only.

{
  "summary": "Overall assessment of the PR",
  "approval_recommendation": "APPROVE|REQUEST_CHANGES|COMMENT",
  "stats": {
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "info": 0
  },
  "comments": [
    {
      "severity": "Critical|High|Medium|Low|Info",
      "category": "Bug|Security|Performance|Style|Maintainability",
      "file": "path/to/file.py",
      "line": 42,
      "title": "Brief issue title",
      "description": "Detailed description of the issue",
      "suggestion": "How to fix it",
      "code_suggestion": "Optional code snippet",
      "confidence": 85
    }
  ],
  "positive_feedback": ["List of things done well"]
}

PULL REQUEST INFO:
Title: {pr_title}
Description: {pr_description}

CODE DIFF:
{diff_content}
```

### Example Input

```diff
diff --git a/app/auth.py b/app/auth.py
index 1234567..abcdefg 100644
--- a/app/auth.py
+++ b/app/auth.py
@@ -15,6 +15,20 @@ class AuthService:
     def __init__(self, db: Database):
         self.db = db
 
+    def login(self, email: str, password: str) -> dict:
+        query = f"SELECT * FROM users WHERE email = '{email}'"
+        user = self.db.execute(query)
+        
+        if user and user.password == password:
+            token = self.generate_token(user.id)
+            return {"success": True, "token": token}
+        
+        return {"success": False, "error": "Invalid credentials"}
+
+    def generate_token(self, user_id: str) -> str:
+        return base64.b64encode(f"{user_id}:{time.time()}".encode()).decode()
+
     def logout(self, token: str) -> bool:
         # Implementation here
         pass
```

### Example Output

```json
{
  "summary": "This PR introduces a login function with critical security vulnerabilities that must be addressed before merging. The code has SQL injection and plaintext password comparison issues.",
  "approval_recommendation": "REQUEST_CHANGES",
  "stats": {
    "critical": 2,
    "high": 1,
    "medium": 1,
    "low": 0,
    "info": 1
  },
  "comments": [
    {
      "severity": "Critical",
      "category": "Security",
      "file": "app/auth.py",
      "line": 19,
      "title": "SQL Injection Vulnerability",
      "description": "The query uses string formatting to insert user input directly into SQL, allowing SQL injection attacks. An attacker could input `' OR '1'='1` to bypass authentication.",
      "suggestion": "Use parameterized queries or an ORM to prevent SQL injection.",
      "code_suggestion": "query = \"SELECT * FROM users WHERE email = ?\"\nuser = self.db.execute(query, (email,))",
      "confidence": 99
    },
    {
      "severity": "Critical",
      "category": "Security",
      "file": "app/auth.py",
      "line": 22,
      "title": "Plaintext Password Comparison",
      "description": "Passwords are being compared in plaintext. This implies passwords are stored unhashed in the database, which is a severe security risk.",
      "suggestion": "Use a secure password hashing library like bcrypt or argon2 to hash and verify passwords.",
      "code_suggestion": "from passlib.hash import bcrypt\n\nif user and bcrypt.verify(password, user.password_hash):",
      "confidence": 98
    },
    {
      "severity": "High",
      "category": "Security",
      "file": "app/auth.py",
      "line": 28,
      "title": "Insecure Token Generation",
      "description": "The token is just base64-encoded user_id and timestamp, which is easily decodable and forgeable. Anyone can create valid tokens for any user.",
      "suggestion": "Use JWT with a secret key, or use a cryptographically secure random token stored in a session store.",
      "code_suggestion": "import jwt\nimport os\n\ndef generate_token(self, user_id: str) -> str:\n    return jwt.encode(\n        {\"user_id\": user_id, \"exp\": time.time() + 3600},\n        os.environ[\"JWT_SECRET\"],\n        algorithm=\"HS256\"\n    )",
      "confidence": 95
    },
    {
      "severity": "Medium",
      "category": "Maintainability",
      "file": "app/auth.py",
      "line": 18,
      "title": "Missing Input Validation",
      "description": "The function doesn't validate that email and password are non-empty strings before processing.",
      "suggestion": "Add input validation at the start of the function.",
      "code_suggestion": "def login(self, email: str, password: str) -> dict:\n    if not email or not isinstance(email, str):\n        return {\"success\": False, \"error\": \"Invalid email\"}\n    if not password or not isinstance(password, str):\n        return {\"success\": False, \"error\": \"Invalid password\"}",
      "confidence": 90
    },
    {
      "severity": "Info",
      "category": "Style",
      "file": "app/auth.py",
      "line": 18,
      "title": "Consider Using Type Hints for Return Type",
      "description": "The return type could be more specific using TypedDict or a dataclass.",
      "suggestion": "Define a LoginResult type for better type safety.",
      "code_suggestion": "from typing import TypedDict\n\nclass LoginResult(TypedDict):\n    success: bool\n    token: str | None\n    error: str | None",
      "confidence": 70
    }
  ],
  "positive_feedback": [
    "Good separation of concerns with AuthService class",
    "Return format is consistent between success and failure cases",
    "Method names are clear and descriptive"
  ]
}
```

---

## 4. Defect/Issue Creation

### Purpose
Parse CI/test logs and generate a structured defect report with reproduction steps.

### Prompt Template

```
SYSTEM:
You are a QA engineer skilled at analyzing test failures and CI logs. You create clear, actionable bug reports that help developers quickly understand and fix issues.

CONTEXT:
You are analyzing a CI/CD pipeline failure or test failure log. Your task is to:
- Identify the root cause of the failure
- Extract relevant error messages and stack traces
- Determine reproduction steps if possible
- Assess severity and priority
- Suggest potential fixes or investigation areas

TASK:
Analyze the following log and create a defect report.

OUTPUT FORMAT:
Respond with valid JSON only.

{
  "title": "Clear, concise issue title",
  "severity": "Critical|High|Medium|Low",
  "priority": "P0|P1|P2|P3",
  "type": "Bug|Test Failure|Infrastructure|Flaky Test",
  "component": "Affected component or module",
  "description": "Detailed description of the issue",
  "error_message": "The actual error message from logs",
  "stack_trace": "Relevant stack trace if available",
  "reproduction_steps": [
    "Step 1",
    "Step 2"
  ],
  "expected_behavior": "What should happen",
  "actual_behavior": "What actually happened",
  "environment": {
    "os": "OS if known",
    "python_version": "Version if known",
    "commit": "Commit SHA if available",
    "branch": "Branch name"
  },
  "possible_causes": ["Possible cause 1", "Possible cause 2"],
  "suggested_fixes": ["Suggestion 1", "Suggestion 2"],
  "related_files": ["file1.py", "file2.py"],
  "labels": ["bug", "test-failure", "etc"],
  "confidence": 85
}

CI LOG:
{log_content}
```

### Example Input

```
=========================== FAILED TESTS ===========================
_________________ TestUserService.test_create_user _________________

    def test_create_user(self, db_session):
        user_service = UserService(db_session)
        
        user = user_service.create_user(
            email="test@example.com",
            password="Password123"
        )
        
>       assert user.id is not None
E       AttributeError: 'NoneType' object has no attribute 'id'

tests/test_user_service.py:25: AttributeError

--------------------------- Captured log ---------------------------
ERROR    app.services.user:user_service.py:42 Database error: duplicate key value violates unique constraint "users_email_key"
DETAIL:  Key (email)=(test@example.com) already exists.

========================= short test summary =========================
FAILED tests/test_user_service.py::TestUserService::test_create_user
==================== 1 failed, 23 passed in 4.52s ====================

Build: #1234
Branch: feature/user-registration
Commit: abc123def456
```

### Example Output

```json
{
  "title": "test_create_user fails due to duplicate email constraint violation",
  "severity": "Medium",
  "priority": "P2",
  "type": "Test Failure",
  "component": "UserService",
  "description": "The test_create_user test is failing because it's attempting to create a user with an email that already exists in the database. This indicates either a test isolation issue (previous test data not cleaned up) or missing test fixtures.",
  "error_message": "AttributeError: 'NoneType' object has no attribute 'id'",
  "stack_trace": "tests/test_user_service.py:25: AttributeError\nERROR app.services.user:user_service.py:42 Database error: duplicate key value violates unique constraint \"users_email_key\"",
  "reproduction_steps": [
    "Run the test suite with: pytest tests/test_user_service.py",
    "Or run specifically: pytest tests/test_user_service.py::TestUserService::test_create_user",
    "Test fails on second run if database is not reset between runs"
  ],
  "expected_behavior": "create_user should return a User object with a valid id when given valid email and password",
  "actual_behavior": "create_user returns None because the database insert fails due to duplicate email, and the test crashes when accessing .id on None",
  "environment": {
    "os": "Unknown",
    "python_version": "Unknown",
    "commit": "abc123def456",
    "branch": "feature/user-registration"
  },
  "possible_causes": [
    "Test database not properly reset between test runs",
    "Missing @pytest.fixture with scope='function' for db_session",
    "Hardcoded test email conflicts with seed data",
    "create_user method silently returns None on error instead of raising exception"
  ],
  "suggested_fixes": [
    "Add database cleanup in test fixture: db_session.query(User).filter_by(email='test@example.com').delete()",
    "Use unique emails per test: email=f'test_{uuid.uuid4()}@example.com'",
    "Fix create_user to raise an exception on database errors instead of returning None",
    "Add proper transaction rollback in the db_session fixture"
  ],
  "related_files": [
    "tests/test_user_service.py",
    "app/services/user_service.py"
  ],
  "labels": [
    "bug",
    "test-failure",
    "database",
    "test-isolation"
  ],
  "confidence": 92
}
```

---

## Output Schemas

### TestCase Schema

```typescript
interface TestCase {
  id: string;              // Format: TC_XXX
  title: string;           // Descriptive title
  priority: "High" | "Medium" | "Low";
  type: "Positive" | "Negative" | "Edge" | "Boundary";
  preconditions: string[];
  steps: {
    step: number;
    action: string;
    data: string | null;
  }[];
  expected_results: string[];
  postconditions: string[];
}

interface TestCaseResponse {
  requirement_summary: string;
  test_cases: TestCase[];
  coverage_notes: string;
}
```

### PRReview Schema

```typescript
interface ReviewComment {
  severity: "Critical" | "High" | "Medium" | "Low" | "Info";
  category: "Bug" | "Security" | "Performance" | "Style" | "Maintainability";
  file: string;
  line: number;
  title: string;
  description: string;
  suggestion: string;
  code_suggestion?: string;
  confidence: number;  // 0-100
}

interface PRReviewResponse {
  summary: string;
  approval_recommendation: "APPROVE" | "REQUEST_CHANGES" | "COMMENT";
  stats: {
    critical: number;
    high: number;
    medium: number;
    low: number;
    info: number;
  };
  comments: ReviewComment[];
  positive_feedback: string[];
}
```

### DefectReport Schema

```typescript
interface DefectReport {
  title: string;
  severity: "Critical" | "High" | "Medium" | "Low";
  priority: "P0" | "P1" | "P2" | "P3";
  type: "Bug" | "Test Failure" | "Infrastructure" | "Flaky Test";
  component: string;
  description: string;
  error_message: string;
  stack_trace: string;
  reproduction_steps: string[];
  expected_behavior: string;
  actual_behavior: string;
  environment: {
    os?: string;
    python_version?: string;
    commit?: string;
    branch?: string;
  };
  possible_causes: string[];
  suggested_fixes: string[];
  related_files: string[];
  labels: string[];
  confidence: number;  // 0-100
}
```

---

## Provider-Specific Notes

### Google Gemini

```python
# Gemini works well with these prompts as-is
# Use gemini-1.5-flash for speed, gemini-1.5-pro for quality

import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content(
    prompt,
    generation_config={
        "temperature": 0.2,  # Lower for more consistent output
        "top_p": 0.8,
        "max_output_tokens": 4096,
    }
)
```

### Groq (Llama 3.1)

```python
# Groq/Llama may need slightly more explicit JSON formatting instructions
# Add to system prompt: "You must respond with valid JSON only. Do not include markdown code blocks."

from groq import Groq

client = Groq(api_key=GROQ_API_KEY)
response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.2,
    max_tokens=4096,
    response_format={"type": "json_object"}  # If supported
)
```

### OpenAI

```python
# OpenAI supports function calling for more reliable JSON output

from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.2,
    response_format={"type": "json_object"}
)
```

---

## Prompt Versioning

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-10 | Initial prompts for test generation, PR review, defect creation |

### How to Update Prompts

1. Test new prompt version with sample inputs
2. Compare output quality with previous version
3. Update version number and changelog
4. Deploy gradually (A/B test if possible)

### Testing Prompts

```python
# prompt_test.py
import json

def test_prompt_output(prompt: str, llm_response: str) -> bool:
    """Validate that LLM output matches expected schema."""
    try:
        data = json.loads(llm_response)
        # Add schema validation here
        return True
    except json.JSONDecodeError:
        return False
```

---

## Tips for Prompt Engineering

### Do's ✅
- Be specific about output format
- Include examples (few-shot learning)
- Set clear constraints
- Use structured output (JSON)
- Test with edge cases
- Version control your prompts

### Don'ts ❌
- Don't be vague about expectations
- Don't assume the model knows your domain
- Don't skip validation of outputs
- Don't use prompts without testing
- Don't forget to handle errors

---

## Related Files

- `backend/prompts/` — Prompt template files (to be created)
- `backend/schemas/` — Pydantic models for output validation (to be created)
- `tests/test_prompts.py` — Prompt output tests (to be created)
