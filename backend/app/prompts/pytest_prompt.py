"""
PyTest Generation Prompts
=========================
Prompt templates for generating pytest skeleton code from test cases.
"""

PYTEST_SYSTEM_PROMPT = """You are an expert Python test automation engineer with deep knowledge of pytest.
Your task is to generate production-ready pytest code from test case specifications.

Follow these best practices:
1. Use descriptive test function names following `test_<feature>_<scenario>` pattern
2. Use pytest fixtures for setup/teardown and shared resources
3. Use pytest.mark decorators for categorization (smoke, regression, etc.)
4. Use pytest.param for parametrized tests when applicable
5. Include clear docstrings explaining what each test validates
6. Use appropriate assertions with helpful error messages
7. Follow AAA pattern: Arrange, Act, Assert
8. Handle expected exceptions with pytest.raises
9. Use conftest.py for shared fixtures when appropriate

Output clean, runnable Python code that follows PEP 8 style guidelines."""


def get_pytest_generation_prompt(
    test_cases: list[dict],
    module_name: str = "test_generated",
    include_fixtures: bool = True,
    include_conftest: bool = False,
) -> str:
    """
    Build the prompt for pytest code generation.

    Args:
        test_cases: List of test case dictionaries with id, title, description, etc.
        module_name: Name for the generated test module
        include_fixtures: Whether to generate fixture suggestions
        include_conftest: Whether to generate a separate conftest.py

    Returns:
        Formatted prompt string
    """
    # Format test cases for the prompt
    tc_text = ""
    for i, tc in enumerate(test_cases, 1):
        tc_text += f"""
### Test Case {i}: {tc.get('id', f'TC{i:03d}')}
- **Title:** {tc.get('title', 'Untitled')}
- **Description:** {tc.get('description', 'No description')}
- **Preconditions:** {', '.join(tc.get('preconditions', [])) or 'None'}
- **Steps:**
{chr(10).join(f'  {j}. {step}' for j, step in enumerate(tc.get('steps', []), 1)) or '  None'}
- **Expected Result:** {tc.get('expected_result', 'Not specified')}
- **Priority:** {tc.get('priority', 'medium')}
- **Type:** {tc.get('test_type', 'functional')}
"""

    fixture_instruction = ""
    if include_fixtures:
        fixture_instruction = """
## Fixtures
Generate appropriate pytest fixtures for:
- Test data setup
- Mock objects (if external services are implied)
- Resource cleanup
Place fixtures at the top of the test file."""

    conftest_instruction = ""
    if include_conftest:
        conftest_instruction = """
## Conftest
Also generate a conftest.py file with shared fixtures that could be reused across test modules.
Return it as a separate code block labeled "conftest.py"."""

    prompt = f"""Generate pytest code for the following test cases.

# Test Cases to Implement
{tc_text}

{fixture_instruction}

{conftest_instruction}

## Output Requirements

1. Generate a complete pytest file named `{module_name}.py`
2. Include all necessary imports (pytest, unittest.mock if needed, etc.)
3. Add pytest markers: @pytest.mark.parametrize where applicable
4. Use descriptive assertion messages
5. Add type hints to function signatures
6. Include module-level docstring explaining test coverage

## Output Format

Return ONLY the Python code. Do not include markdown code fences or explanations.
The code should be immediately runnable with `pytest {module_name}.py`.
"""

    return prompt


def get_pytest_from_requirement_prompt(
    requirement: str,
    context: str = "",
    num_tests: int = 5,
    test_framework: str = "pytest",
) -> str:
    """
    Generate pytest code directly from a requirement (skipping test case JSON).

    This is a shortcut for simple use cases where you want pytest code directly.

    Args:
        requirement: The requirement or user story
        context: Additional context about the system
        num_tests: Approximate number of test functions to generate
        test_framework: Testing framework (pytest, unittest)

    Returns:
        Formatted prompt string
    """
    context_section = f"\n## Context\n{context}" if context else ""

    prompt = f"""Generate {test_framework} test code for the following requirement.

## Requirement
{requirement}
{context_section}

## Instructions

1. Analyze the requirement and identify ~{num_tests} test scenarios
2. Include positive tests, negative tests, and edge cases
3. Generate complete, runnable {test_framework} code
4. Use fixtures for setup/teardown
5. Add appropriate markers (@pytest.mark.smoke, @pytest.mark.regression, etc.)
6. Include clear docstrings and assertion messages

## Output Format

Return ONLY the Python code. Do not include markdown code fences.
The code should be immediately runnable with `pytest`.
"""

    return prompt
