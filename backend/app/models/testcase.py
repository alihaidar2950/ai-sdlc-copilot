"""
Test Case Models
================
Pydantic models for test case generation request/response.
"""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """Test case priority levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TestCaseType(str, Enum):
    """Test case types."""

    FUNCTIONAL = "functional"
    EDGE_CASE = "edge_case"
    NEGATIVE = "negative"
    SECURITY = "security"
    PERFORMANCE = "performance"


class TestCase(BaseModel):
    """A single generated test case."""

    id: str = Field(..., description="Unique test case ID (e.g., TC001)")
    title: str = Field(..., description="Brief test case title")
    description: str = Field(..., description="What this test validates")
    preconditions: list[str] = Field(default_factory=list, description="Setup requirements")
    steps: list[str] = Field(..., description="Step-by-step test instructions")
    expected_result: str = Field(..., description="Expected outcome")
    priority: Priority = Field(default=Priority.MEDIUM, description="Test priority")
    test_type: TestCaseType = Field(default=TestCaseType.FUNCTIONAL, description="Type of test")


class TestCaseGenerateRequest(BaseModel):
    """Request to generate test cases from a requirement."""

    requirement: str = Field(
        ...,
        description="The requirement or user story to generate test cases for",
        min_length=10,
    )
    context: str = Field(
        default="",
        description="Additional context about the system, tech stack, or constraints",
    )
    num_cases: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of test cases to generate",
    )
    include_edge_cases: bool = Field(
        default=True,
        description="Include edge case and negative test scenarios",
    )
    output_format: Literal["json", "markdown"] = Field(
        default="json",
        description="Output format: json (structured) or markdown (human-readable)",
    )
    system_prompt: str | None = Field(
        default=None,
        description="Override the default QA engineer system prompt (for advanced users)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "requirement": "User should be able to login with email and password",
                    "context": "",
                    "num_cases": 5,
                    "include_edge_cases": True,
                    "output_format": "json",
                    "system_prompt": "You are an expert QA engineer with 10+ years of experience in test case design. Your task is to generate comprehensive, production-ready test cases from software requirements.",
                }
            ]
        }
    }


class TestCaseGenerateResponse(BaseModel):
    """Response containing generated test cases."""

    requirement: str = Field(..., description="The original requirement")
    test_cases: list[TestCase] = Field(..., description="Generated test cases")
    total_count: int = Field(..., description="Number of test cases generated")
    llm_provider: str = Field(..., description="Which LLM was used (groq/gemini)")
