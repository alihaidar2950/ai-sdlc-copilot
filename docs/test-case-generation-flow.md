# Test Case Generation - Architecture & Data Flow

This document explains how the test case generation feature works in AI SDLC Co-Pilot.

---

## High-Level Architecture

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        USER["User/Frontend"]
    end
    
    subgraph API["API Layer"]
        MAIN["main.py<br/>FastAPI App"]
        ROUTER["routers/testcases.py<br/>API Endpoint"]
    end
    
    subgraph Business["Business Logic Layer"]
        MODELS["models/testcase.py<br/>Data Validation"]
        PROMPTS["prompts/testcase_prompt.py<br/>LLM Instructions"]
        SERVICE["services/llm_service.py<br/>LLM Integration"]
    end
    
    subgraph External["External Services"]
        GROQ["Groq API<br/>Llama 3.3 70B"]
        GEMINI["Google Gemini<br/>Fallback"]
    end
    
    USER -->|"POST /api/v1/testcases/generate"| MAIN
    MAIN -->|"Route request"| ROUTER
    ROUTER -->|"Validate input"| MODELS
    ROUTER -->|"Build prompt"| PROMPTS
    ROUTER -->|"Generate"| SERVICE
    SERVICE -->|"Primary"| GROQ
    SERVICE -.->|"Fallback"| GEMINI
    SERVICE -->|"Response"| ROUTER
    ROUTER -->|"Validate output"| MODELS
    ROUTER -->|"JSON Response"| USER
```

---

## Request/Response Flow

```mermaid
sequenceDiagram
    participant U as User
    participant M as main.py
    participant R as routers/testcases.py
    participant Mo as models/testcase.py
    participant P as prompts/testcase_prompt.py
    participant S as services/llm_service.py
    participant G as Groq API

    U->>M: POST /api/v1/testcases/generate
    Note over U,M: {"requirement": "Login feature..."}
    
    M->>R: Route to testcases router
    R->>Mo: Validate TestCaseGenerateRequest
    Mo-->>R: ✅ Valid request
    
    R->>P: get_testcase_generation_prompt()
    P-->>R: Formatted prompt string
    
    R->>S: llm.generate(prompt, system_prompt)
    S->>G: Chat completion request
    G-->>S: JSON with test cases
    S-->>R: Raw response text
    
    R->>R: Parse JSON response
    
    loop For each test case
        R->>Mo: Validate TestCase model
        Mo-->>R: ✅ Valid test case
    end
    
    R->>Mo: Build TestCaseGenerateResponse
    Mo-->>R: ✅ Valid response
    
    R-->>U: 200 OK + JSON response
```

---

## File Responsibilities

```mermaid
flowchart LR
    subgraph main["main.py"]
        direction TB
        M1["Create FastAPI app"]
        M2["Register routers"]
        M3["Configure CORS"]
    end
    
    subgraph router["routers/testcases.py"]
        direction TB
        R1["Define endpoint"]
        R2["Orchestrate flow"]
        R3["Handle errors"]
        R4["Parse LLM response"]
    end
    
    subgraph models["models/testcase.py"]
        direction TB
        MO1["TestCaseGenerateRequest"]
        MO2["TestCaseGenerateResponse"]
        MO3["TestCase"]
        MO4["Priority enum"]
        MO5["TestCaseType enum"]
    end
    
    subgraph prompts["prompts/testcase_prompt.py"]
        direction TB
        P1["TESTCASE_SYSTEM_PROMPT"]
        P2["get_testcase_generation_prompt()"]
    end
    
    subgraph service["services/llm_service.py"]
        direction TB
        S1["LLMService class"]
        S2["generate()"]
        S3["_generate_groq()"]
        S4["_generate_gemini()"]
    end
    
    main --> router
    router --> models
    router --> prompts
    router --> service
```

---

## Data Transformation Pipeline

```mermaid
flowchart TB
    subgraph Input["1. User Input"]
        IN[/"JSON Request"/]
        IN_EX["requirement: 'User login...'<br/>num_cases: 5<br/>include_edge_cases: true"]
    end
    
    subgraph Validate["2. Input Validation"]
        VAL["TestCaseGenerateRequest<br/>Pydantic Model"]
        VAL_CHECK["✅ min_length=10<br/>✅ num_cases 1-20<br/>✅ Required fields"]
    end
    
    subgraph Prompt["3. Prompt Construction"]
        SYS["System Prompt:<br/>'You are an expert QA engineer...'"]
        USR["User Prompt:<br/>'Generate 5 test cases for...'"]
    end
    
    subgraph LLM["4. LLM Processing"]
        GROQ["Groq Llama 3.3"]
        GEN["Generate JSON response"]
    end
    
    subgraph Parse["5. Response Parsing"]
        RAW["Raw JSON string"]
        CLEAN["Remove markdown if present"]
        PARSE["json.loads()"]
    end
    
    subgraph ValidateOut["6. Output Validation"]
        TC["TestCase model × 5"]
        RESP["TestCaseGenerateResponse"]
    end
    
    subgraph Output["7. API Response"]
        OUT[/"JSON Response"/]
    end
    
    Input --> Validate
    Validate --> Prompt
    Prompt --> LLM
    LLM --> Parse
    Parse --> ValidateOut
    ValidateOut --> Output
```

---

## Model Relationships

```mermaid
classDiagram
    class TestCaseGenerateRequest {
        +str requirement
        +str context
        +int num_cases
        +bool include_edge_cases
    }
    
    class TestCaseGenerateResponse {
        +str requirement
        +List~TestCase~ test_cases
        +int total_count
        +str llm_provider
    }
    
    class TestCase {
        +str id
        +str title
        +str description
        +List~str~ preconditions
        +List~str~ steps
        +str expected_result
        +Priority priority
        +TestCaseType test_type
    }
    
    class Priority {
        <<enumeration>>
        HIGH
        MEDIUM
        LOW
    }
    
    class TestCaseType {
        <<enumeration>>
        FUNCTIONAL
        EDGE_CASE
        NEGATIVE
        SECURITY
        PERFORMANCE
    }
    
    TestCaseGenerateResponse --> TestCase : contains
    TestCase --> Priority : has
    TestCase --> TestCaseType : has
```

---

## LLM Fallback Strategy

```mermaid
flowchart TD
    START["generate() called"]
    
    CHECK_GROQ{"Groq client<br/>configured?"}
    TRY_GROQ["Try Groq API"]
    GROQ_OK{"Success?"}
    
    CHECK_GEMINI{"Gemini client<br/>configured?"}
    TRY_GEMINI["Try Gemini API"]
    GEMINI_OK{"Success?"}
    
    RETURN["Return response"]
    ERROR["Raise ValueError"]
    
    START --> CHECK_GROQ
    CHECK_GROQ -->|Yes| TRY_GROQ
    CHECK_GROQ -->|No| CHECK_GEMINI
    
    TRY_GROQ --> GROQ_OK
    GROQ_OK -->|Yes| RETURN
    GROQ_OK -->|No| CHECK_GEMINI
    
    CHECK_GEMINI -->|Yes| TRY_GEMINI
    CHECK_GEMINI -->|No| ERROR
    
    TRY_GEMINI --> GEMINI_OK
    GEMINI_OK -->|Yes| RETURN
    GEMINI_OK -->|No| ERROR
    
    style RETURN fill:#90EE90
    style ERROR fill:#FFB6C1
```

---

## Example Request/Response

### Request
```json
POST /api/v1/testcases/generate
{
    "requirement": "User should be able to login with email and password",
    "num_cases": 5,
    "include_edge_cases": true
}
```

### Internal Prompt (sent to LLM)
```
System: You are an expert QA engineer specializing in test case design...

User: Generate exactly 5 test cases for the following requirement.

Requirement:
User should be able to login with email and password

Include a mix of:
- Functional tests (happy path)
- Edge cases (boundary conditions)
- Negative tests (invalid inputs, error handling)
- Security tests (if applicable)

Respond with ONLY this JSON structure...
```

### Response
```json
{
    "requirement": "User should be able to login with email and password",
    "test_cases": [
        {
            "id": "TC001",
            "title": "Successful Login with Valid Credentials",
            "description": "Validates user login with correct email and password",
            "preconditions": ["User has a valid account", "User is on login page"],
            "steps": ["Enter valid email", "Enter valid password", "Click login"],
            "expected_result": "User is logged in and redirected to dashboard",
            "priority": "high",
            "test_type": "functional"
        }
        // ... 4 more test cases
    ],
    "total_count": 5,
    "llm_provider": "groq"
}
```

---

## File Structure

```
backend/app/
├── main.py                      # FastAPI app entry point
│   └── Imports and registers testcases router
│
├── routers/
│   ├── __init__.py
│   └── testcases.py             # POST /api/v1/testcases/generate
│       ├── Validates request using models
│       ├── Builds prompt using prompts module
│       ├── Calls LLM service
│       ├── Parses JSON response
│       └── Returns validated response
│
├── models/
│   ├── __init__.py
│   └── testcase.py              # Pydantic models
│       ├── Priority (enum)
│       ├── TestCaseType (enum)
│       ├── TestCase (model)
│       ├── TestCaseGenerateRequest (model)
│       └── TestCaseGenerateResponse (model)
│
├── prompts/
│   ├── __init__.py
│   └── testcase_prompt.py       # LLM prompt templates
│       ├── TESTCASE_SYSTEM_PROMPT (constant)
│       └── get_testcase_generation_prompt() (function)
│
└── services/
    ├── __init__.py
    └── llm_service.py           # LLM integration
        ├── LLMService (class)
        │   ├── generate()
        │   ├── _generate_groq()
        │   └── _generate_gemini()
        └── get_llm_service() (singleton factory)
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Pydantic models** | Automatic validation, OpenAPI docs, type safety |
| **Separate prompts file** | Easy to iterate on prompts without touching code |
| **Router pattern** | Organize endpoints by feature, scalable |
| **Service layer** | Decouple LLM logic from HTTP handling |
| **Singleton LLM service** | Reuse client connections, avoid re-initialization |
| **Fallback strategy** | Resilience if primary LLM fails |
| **JSON output from LLM** | Structured, parseable, validatable |
