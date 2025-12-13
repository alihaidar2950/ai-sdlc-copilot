"""
Test Case Generation Prompt
===========================
Prompt template for generating test cases from requirements.
"""

TESTCASE_SYSTEM_PROMPT = """You are an expert QA engineer specializing in test case design.
Your task is to generate comprehensive test cases from software requirements.

You must respond with ONLY valid JSON, no markdown, no explanations.

Guidelines:
- Create clear, actionable test cases
- Include positive, negative, and edge cases
- Use specific, measurable expected results
- Consider security and error handling scenarios
- Prioritize based on business impact"""


def get_testcase_generation_prompt(
    requirement: str,
    num_cases: int = 5,
    include_edge_cases: bool = True,
    context: str | None = None,
) -> str:
    """
    Generate the prompt for test case generation.

    Args:
        requirement: The requirement or user story
        num_cases: Number of test cases to generate
        include_edge_cases: Whether to include edge/negative cases
        context: Additional context about the system

    Returns:
        Formatted prompt string
    """
    edge_case_instruction = ""
    if include_edge_cases:
        edge_case_instruction = """
Include a mix of:
- Functional tests (happy path)
- Edge cases (boundary conditions)
- Negative tests (invalid inputs, error handling)
- Security tests (if applicable)"""

    context_section = ""
    if context:
        context_section = f"""
System Context:
{context}
"""

    return f"""Generate exactly {num_cases} test cases for the following requirement.
{context_section}
Requirement:
{requirement}
{edge_case_instruction}

Respond with ONLY this JSON structure (no markdown, no code blocks):
{{
    "test_cases": [
        {{
            "id": "TC001",
            "title": "Brief descriptive title",
            "description": "What this test validates",
            "preconditions": ["Any setup required"],
            "steps": ["Step 1", "Step 2", "Step 3"],
            "expected_result": "Clear expected outcome",
            "priority": "high|medium|low",
            "test_type": "functional|edge_case|negative|security|performance"
        }}
    ]
}}"""
