/**
 * API Service for AI SDLC Co-Pilot Backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1"

// Types
export interface TestCase {
  id: string
  title: string
  description: string
  preconditions: string[]
  steps: string[]
  expected_result: string
  priority: "critical" | "high" | "medium" | "low"
  test_type: "functional" | "integration" | "e2e" | "smoke" | "regression"
}

export interface GenerateTestCasesRequest {
  requirement: string
  context?: string
  test_types?: string[]
  num_cases?: number
}

export interface GenerateTestCasesResponse {
  requirement: string
  test_cases: TestCase[]
  metadata: {
    generated_at: string
    model: string
    count: number
  }
}

export interface PyTestGenerateRequest {
  test_cases: {
    id: string
    title: string
    description: string
    preconditions?: string[]
    steps?: string[]
    expected_result: string
    priority?: string
    test_type?: string
  }[]
  module_name?: string
  output_path?: string
  include_fixtures?: boolean
  include_conftest?: boolean
}

export interface PyTestGenerateResponse {
  code: string
  module_name: string
  test_count: number
  conftest_code?: string
  saved_to?: string
}

export interface ApiStatus {
  app: string
  version: string
  environment: string
  debug: boolean
  timestamp: string
}

// API Functions
class ApiService {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Unknown error" }))
      throw new Error(error.detail || `HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  // Status
  async getStatus(): Promise<ApiStatus> {
    return this.request<ApiStatus>("/status")
  }

  // Test Case Generation
  async generateTestCases(
    request: GenerateTestCasesRequest
  ): Promise<GenerateTestCasesResponse> {
    return this.request<GenerateTestCasesResponse>("/testcases/generate", {
      method: "POST",
      body: JSON.stringify(request),
    })
  }

  // PyTest Generation
  async generatePyTest(
    request: PyTestGenerateRequest
  ): Promise<PyTestGenerateResponse> {
    return this.request<PyTestGenerateResponse>("/pytest/generate", {
      method: "POST",
      body: JSON.stringify(request),
    })
  }

  // Generate PyTest directly from requirement
  async generatePyTestFromRequirement(
    requirement: string,
    context?: string,
    outputPath?: string,
    moduleName?: string
  ): Promise<PyTestGenerateResponse> {
    return this.request<PyTestGenerateResponse>(
      "/pytest/generate-from-requirement",
      {
        method: "POST",
        body: JSON.stringify({
          requirement,
          context,
          output_path: outputPath,
          module_name: moduleName,
        }),
      }
    )
  }
}

export const api = new ApiService()
export default api
