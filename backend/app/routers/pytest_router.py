"""
PyTest Generation Router
========================
API endpoints for generating pytest skeleton code from test cases.
"""

import logging
import re
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.models.pytest_models import (
    PyTestFromRequirementRequest,
    PyTestGenerateRequest,
    PyTestGenerateResponse,
)
from app.prompts.pytest_prompt import (
    PYTEST_SYSTEM_PROMPT,
    get_pytest_from_requirement_prompt,
    get_pytest_generation_prompt,
)
from app.services.llm_service import get_llm_service

router = APIRouter(prefix="/pytest", tags=["PyTest"])
logger = logging.getLogger("ai_sdlc_copilot")


def save_code_to_file(
    code: str,
    output_path: str,
    filename: str,
    conftest_code: str | None = None,
) -> str:
    """
    Save generated code to a file.

    Args:
        code: The pytest code to save
        output_path: Directory path to save to
        filename: Name of the file (without .py)
        conftest_code: Optional conftest.py content

    Returns:
        Full path to the saved file
    """
    # Create directory if it doesn't exist
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save main test file
    file_path = output_dir / f"{filename}.py"
    file_path.write_text(code, encoding="utf-8")
    logger.info(f"📁 Saved pytest code to: {file_path}")

    # Save conftest if provided
    if conftest_code:
        conftest_path = output_dir / "conftest.py"
        conftest_path.write_text(conftest_code, encoding="utf-8")
        logger.info(f"📁 Saved conftest.py to: {conftest_path}")

    return str(file_path.resolve())


def clean_code_response(response: str) -> str:
    """
    Clean up LLM response to extract pure Python code.
    Removes markdown code fences and extra whitespace.
    """
    # Remove markdown code fences if present
    cleaned = response.strip()

    # Handle ```python ... ``` blocks
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first line (```python or ```)
        lines = lines[1:]
        # Remove last line if it's ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines)

    return cleaned.strip()


def count_test_functions(code: str) -> int:
    """Count the number of test functions in the generated code."""
    # Match function definitions starting with 'test_'
    pattern = r"^(?:async\s+)?def\s+test_\w+\s*\("
    matches = re.findall(pattern, code, re.MULTILINE)
    return len(matches)


@router.post("/generate", response_model=PyTestGenerateResponse)
async def generate_pytest_from_testcases(request: PyTestGenerateRequest):
    """
    Generate pytest skeleton code from test case specifications.

    This endpoint takes structured test cases (with steps, expected results, etc.)
    and generates runnable pytest code.

    **Example workflow:**
    1. Generate test cases using `/api/v1/testcases/generate`
    2. Pass those test cases to this endpoint
    3. Get back pytest code ready to run

    **Returns:**
    - `code`: The generated pytest Python code
    - `conftest_code`: Optional conftest.py content (if requested)
    - `test_count`: Number of test functions generated
    """
    logger.info(
        f"Generating pytest code for {len(request.test_cases)} test cases -> {request.module_name}.py"
    )

    try:
        # Get LLM service
        llm = get_llm_service()

        # Convert test cases to dict format for prompt
        test_cases_data = [tc.model_dump() for tc in request.test_cases]

        # Build the prompt
        prompt = get_pytest_generation_prompt(
            test_cases=test_cases_data,
            module_name=request.module_name,
            include_fixtures=request.include_fixtures,
            include_conftest=request.include_conftest,
        )

        # Use custom or default system prompt
        system_prompt = request.system_prompt or PYTEST_SYSTEM_PROMPT

        # Generate pytest code
        response_text = await llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=4096,
            temperature=0.3,  # Lower temperature for code generation
        )

        # Determine which provider was used
        llm_provider = "groq" if llm._groq_client else "gemini"

        # Clean the response
        code = clean_code_response(response_text)

        # Handle conftest if requested (split from main response if present)
        conftest_code = None
        if request.include_conftest and "conftest.py" in response_text.lower():
            # Try to extract conftest section
            conftest_match = re.search(
                r"(?:#+\s*conftest\.py|# conftest\.py).*?```python\s*(.*?)```",
                response_text,
                re.IGNORECASE | re.DOTALL,
            )
            if conftest_match:
                conftest_code = conftest_match.group(1).strip()

        # Count test functions
        test_count = count_test_functions(code)

        # Save to file if output_path provided
        saved_to = None
        if request.output_path:
            saved_to = save_code_to_file(
                code=code,
                output_path=request.output_path,
                filename=request.module_name,
                conftest_code=conftest_code,
            )

        logger.info(f"✅ Generated {test_count} test functions using {llm_provider}")

        return PyTestGenerateResponse(
            module_name=request.module_name,
            code=code,
            conftest_code=conftest_code,
            test_count=test_count,
            llm_provider=llm_provider,
            saved_to=saved_to,
        )

    except Exception as e:
        logger.error(f"PyTest generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate pytest code: {str(e)}",
        ) from e


@router.post("/generate-from-requirement", response_model=PyTestGenerateResponse)
async def generate_pytest_from_requirement(request: PyTestFromRequirementRequest):
    """
    Generate pytest code directly from a requirement (shortcut).

    This skips the intermediate test case JSON and generates pytest code
    directly from a requirement. Useful for quick prototyping.

    **For more control**, use the two-step process:
    1. `/api/v1/testcases/generate` - Get structured test cases
    2. `/api/v1/pytest/generate` - Convert to pytest code
    """
    logger.info(f"Generating pytest code directly from requirement -> {request.module_name}.py")

    try:
        # Get LLM service
        llm = get_llm_service()

        # Build the prompt
        prompt = get_pytest_from_requirement_prompt(
            requirement=request.requirement,
            context=request.context,
            num_tests=request.num_tests,
        )

        # Use custom or default system prompt
        system_prompt = request.system_prompt or PYTEST_SYSTEM_PROMPT

        # Generate pytest code
        response_text = await llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=4096,
            temperature=0.3,
        )

        # Determine which provider was used
        llm_provider = "groq" if llm._groq_client else "gemini"

        # Clean the response
        code = clean_code_response(response_text)

        # Count test functions
        test_count = count_test_functions(code)

        # Save to file if output_path provided
        saved_to = None
        if request.output_path:
            saved_to = save_code_to_file(
                code=code,
                output_path=request.output_path,
                filename=request.module_name,
            )

        logger.info(f"✅ Generated {test_count} test functions using {llm_provider}")

        return PyTestGenerateResponse(
            module_name=request.module_name,
            code=code,
            conftest_code=None,
            test_count=test_count,
            llm_provider=llm_provider,
            saved_to=saved_to,
        )

    except Exception as e:
        logger.error(f"PyTest generation from requirement failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate pytest code: {str(e)}",
        ) from e
