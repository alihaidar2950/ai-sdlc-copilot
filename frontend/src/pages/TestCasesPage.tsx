import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Loader2, Sparkles, Copy, Check, ArrowRight } from "lucide-react"
import { useNavigate } from "react-router-dom"
import api, { TestCase, GenerateTestCasesResponse } from "@/services/api"

export function TestCasesPage() {
  const navigate = useNavigate()
  const [requirement, setRequirement] = useState("")
  const [context, setContext] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<GenerateTestCasesResponse | null>(null)
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const handleGenerate = async () => {
    if (!requirement.trim()) {
      setError("Please enter a requirement")
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await api.generateTestCases({
        requirement,
        context: context || undefined,
        num_cases: 5,
      })
      setResult(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate test cases")
    } finally {
      setLoading(false)
    }
  }

  const copyTestCase = async (tc: TestCase) => {
    const text = `
Test Case: ${tc.id}
Title: ${tc.title}
Description: ${tc.description}
Priority: ${tc.priority}
Type: ${tc.test_type}

Preconditions:
${tc.preconditions.map(p => `- ${p}`).join("\n")}

Steps:
${tc.steps.map((s, i) => `${i + 1}. ${s}`).join("\n")}

Expected Result:
${tc.expected_result}
`.trim()

    await navigator.clipboard.writeText(text)
    setCopiedId(tc.id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const generatePyTest = () => {
    if (result?.test_cases) {
      // Store test cases in sessionStorage for the pytest page
      sessionStorage.setItem("testCases", JSON.stringify(result.test_cases))
      navigate("/pytest")
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "critical": return "destructive"
      case "high": return "warning"
      case "medium": return "secondary"
      case "low": return "outline"
      default: return "secondary"
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Test Case Generation</h1>
        <p className="text-muted-foreground mt-2">
          Generate comprehensive test cases from your requirements using AI
        </p>
      </div>

      {/* Input Form */}
      <Card>
        <CardHeader>
          <CardTitle>Enter Requirement</CardTitle>
          <CardDescription>
            Describe the feature or functionality you want to test
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium mb-2 block">
              Requirement <span className="text-destructive">*</span>
            </label>
            <Textarea
              placeholder="e.g., Users should be able to login with email and password. The system should validate credentials and return appropriate error messages for invalid inputs."
              value={requirement}
              onChange={(e) => setRequirement(e.target.value)}
              className="min-h-[120px]"
            />
          </div>

          <div>
            <label className="text-sm font-medium mb-2 block">
              Additional Context <span className="text-muted-foreground">(optional)</span>
            </label>
            <Textarea
              placeholder="e.g., This is for a REST API endpoint, using JWT authentication. The user model has email, password_hash, and is_active fields."
              value={context}
              onChange={(e) => setContext(e.target.value)}
              className="min-h-[80px]"
            />
          </div>

          {error && (
            <div className="text-sm text-destructive bg-destructive/10 p-3 rounded-md">
              {error}
            </div>
          )}

          <Button onClick={handleGenerate} disabled={loading} className="w-full">
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Generate Test Cases
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Results */}
      {result && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold">Generated Test Cases</h2>
              <p className="text-sm text-muted-foreground">
                {result.metadata.count} test cases generated using {result.metadata.model}
              </p>
            </div>
            <Button onClick={generatePyTest}>
              Generate PyTest Code
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>

          <div className="grid gap-4">
            {result.test_cases.map((tc) => (
              <Card key={tc.id}>
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg flex items-center gap-2">
                        <span className="font-mono text-sm text-muted-foreground">
                          {tc.id}
                        </span>
                        {tc.title}
                      </CardTitle>
                      <CardDescription className="mt-1">
                        {tc.description}
                      </CardDescription>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={getPriorityColor(tc.priority) as "default"}>
                        {tc.priority}
                      </Badge>
                      <Badge variant="outline">{tc.test_type}</Badge>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => copyTestCase(tc)}
                      >
                        {copiedId === tc.id ? (
                          <Check className="h-4 w-4 text-green-500" />
                        ) : (
                          <Copy className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {tc.preconditions.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium mb-2">Preconditions</h4>
                      <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
                        {tc.preconditions.map((p, i) => (
                          <li key={i}>{p}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div>
                    <h4 className="text-sm font-medium mb-2">Steps</h4>
                    <ol className="list-decimal list-inside text-sm text-muted-foreground space-y-1">
                      {tc.steps.map((step, i) => (
                        <li key={i}>{step}</li>
                      ))}
                    </ol>
                  </div>

                  <div>
                    <h4 className="text-sm font-medium mb-2">Expected Result</h4>
                    <p className="text-sm text-muted-foreground bg-muted p-3 rounded-md">
                      {tc.expected_result}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
