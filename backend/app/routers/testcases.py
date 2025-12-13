"""
Test Cases Router
=================
API endpoints for test case generation.
"""

import json
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.testcase import (
    TestCase,
    TestCaseGenerateRequest,
    TestCaseGenerateResponse,
)
from app.prompts.testcase_prompt import (
    TESTCASE_SYSTEM_PROMPT,
    get_testcase_generation_prompt,
)
from app.services.llm_service import get_llm_service


class MarkdownResponse(BaseModel):
    """Response containing test cases in markdown format."""

    requirement: str = Field(..., description="The original requirement")
    markdown: str = Field(..., description="Test cases in markdown format")
    total_count: int = Field(..., description="Approximate number of test cases")
    llm_provider: str = Field(..., description="Which LLM was used")


logger = logging.getLogger("ai_sdlc_copilot")

router = APIRouter(prefix="/api/v1/testcases", tags=["Test Cases"])


@router.post("/generate", response_model=TestCaseGenerateResponse | MarkdownResponse)
async def generate_test_cases(request: TestCaseGenerateRequest):
    """
    Generate test cases from a requirement using AI.

    Takes a software requirement and generates comprehensive test cases
    including functional, edge case, and negative scenarios.
    """
    logger.info(f"Generating {request.num_cases} test cases for: {request.requirement[:50]}...")

    try:
        # Get LLM service
        llm = get_llm_service()

        # Build the prompt
        prompt = get_testcase_generation_prompt(
            requirement=request.requirement,
            num_cases=request.num_cases,
            include_edge_cases=request.include_edge_cases,
            context=request.context,
            output_format=request.output_format,
        )

        # Use custom system prompt if provided, otherwise default
        system_prompt = request.system_prompt or TESTCASE_SYSTEM_PROMPT

        # Generate test cases
        response_text = await llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=4096,
            temperature=0.7,
        )

        # Determine which provider was used
        llm_provider = "groq" if llm._groq_client else "gemini"

        # Handle markdown format - return raw text
        if request.output_format == "markdown":
            # Count approximate test cases by counting "## TC" occurrences
            tc_count = response_text.count("## TC")
            if tc_count == 0:
                tc_count = request.num_cases  # Fallback to requested count

            logger.info(f"✅ Generated ~{tc_count} test cases (markdown) using {llm_provider}")

            return MarkdownResponse(
                requirement=request.requirement,
                markdown=response_text,
                total_count=tc_count,
                llm_provider=llm_provider,
            )

        # Parse JSON response
        try:
            # Clean up response (remove markdown code blocks if present)
            cleaned = response_text.strip()
            if cleaned.startswith("```"):
                # Remove ```json and ``` markers
                lines = cleaned.split("\n")
                cleaned = "\n".join(lines[1:-1])

            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Raw response: {response_text[:500]}")
            raise HTTPException(
                status_code=500,
                detail=f"LLM returned invalid JSON. Please try again. Error: {str(e)}",
            ) from None

        # Validate and build test cases
        test_cases = []
        for tc_data in data.get("test_cases", []):
            try:
                test_case = TestCase(
                    id=tc_data.get("id", f"TC{len(test_cases)+1:03d}"),
                    title=tc_data.get("title", "Untitled"),
                    description=tc_data.get("description", ""),
                    preconditions=tc_data.get("preconditions", []),
                    steps=tc_data.get("steps", []),
                    expected_result=tc_data.get("expected_result", ""),
                    priority=tc_data.get("priority", "medium"),
                    test_type=tc_data.get("test_type", "functional"),
                )
                test_cases.append(test_case)
            except Exception as e:
                logger.warning(f"Skipping invalid test case: {e}")
                continue

        if not test_cases:
            raise HTTPException(
                status_code=500,
                detail="No valid test cases could be generated. Please try again.",
            )

        logger.info(f"✅ Generated {len(test_cases)} test cases using {llm_provider}")

        return TestCaseGenerateResponse(
            requirement=request.requirement,
            test_cases=test_cases,
            total_count=len(test_cases),
            llm_provider=llm_provider,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Test case generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test cases: {str(e)}",
        ) from e
