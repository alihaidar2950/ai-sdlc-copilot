"""
PyTest Generation Models
========================
Pydantic models for pytest code generation request/response.
"""

from pydantic import BaseModel, Field


class TestCaseInput(BaseModel):
    """A test case to convert into pytest code."""

    id: str = Field(default="TC001", description="Test case identifier")
    title: str = Field(..., description="Test case title")
    description: str = Field(default="", description="Detailed description")
    preconditions: list[str] = Field(default_factory=list, description="Setup requirements")
    steps: list[str] = Field(default_factory=list, description="Test steps to execute")
    expected_result: str = Field(..., description="Expected outcome")
    priority: str = Field(default="medium", description="Priority: low, medium, high, critical")
    test_type: str = Field(default="functional", description="Type: functional, integration, etc.")


class PyTestGenerateRequest(BaseModel):
    """Request to generate pytest code from test cases."""

    test_cases: list[TestCaseInput] = Field(
        ...,
        description="List of test cases to convert to pytest code",
        min_length=1,
    )
    module_name: str = Field(
        default="test_generated",
        description="Name for the generated test module (without .py)",
        pattern=r"^[a-z][a-z0-9_]*$",
    )
    include_fixtures: bool = Field(
        default=True,
        description="Generate pytest fixtures for setup/teardown",
    )
    include_conftest: bool = Field(
        default=False,
        description="Generate a separate conftest.py with shared fixtures",
    )
    output_path: str = Field(
        default="./tests",
        description="Directory path to save the generated file. Set to empty string to skip saving.",
    )
    system_prompt: str | None = Field(
        default=None,
        description="Override the default system prompt (for advanced users)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "test_cases": [
                        {
                            "id": "TC001",
                            "title": "Valid login with correct credentials",
                            "description": "User should be able to login with valid email and password",
                            "preconditions": ["User exists in database", "User is not locked"],
                            "steps": [
                                "Navigate to login page",
                                "Enter valid email",
                                "Enter valid password",
                                "Click login button",
                            ],
                            "expected_result": "User is redirected to dashboard",
                            "priority": "critical",
                            "test_type": "functional",
                        }
                    ],
                    "module_name": "test_login",
                    "include_fixtures": True,
                    "include_conftest": False,
                    "output_path": "./tests",
                }
            ]
        }
    }


class PyTestGenerateResponse(BaseModel):
    """Response containing generated pytest code."""

    module_name: str = Field(..., description="Name of the generated module")
    code: str = Field(..., description="Generated pytest code")
    conftest_code: str | None = Field(
        default=None,
        description="Generated conftest.py code (if requested)",
    )
    test_count: int = Field(..., description="Number of test functions generated")
    llm_provider: str = Field(..., description="Which LLM was used (groq/gemini)")
    saved_to: str | None = Field(
        default=None,
        description="File path where the code was saved (if output_path was provided)",
    )


class PyTestFromRequirementRequest(BaseModel):
    """Request to generate pytest code directly from a requirement."""

    requirement: str = Field(
        ...,
        description="The requirement or user story to generate tests for",
        min_length=10,
    )
    context: str = Field(
        default="",
        description="Additional context about the system, tech stack, or constraints",
    )
    num_tests: int = Field(
        default=5,
        ge=1,
        le=15,
        description="Approximate number of test functions to generate",
    )
    module_name: str = Field(
        default="test_generated",
        description="Name for the generated test module (without .py)",
        pattern=r"^[a-z][a-z0-9_]*$",
    )
    output_path: str = Field(
        default="./tests",
        description="Directory path to save the generated file. Set to empty string to skip saving.",
    )
    system_prompt: str | None = Field(
        default=None,
        description="Override the default system prompt (for advanced users)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "requirement": "User should be able to reset their password via email",
                    "context": "FastAPI backend, PostgreSQL database, SendGrid for emails",
                    "num_tests": 5,
                    "module_name": "test_password_reset",
                    "output_path": "./tests",
                }
            ]
        }
    }
