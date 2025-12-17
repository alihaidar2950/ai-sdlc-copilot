import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Loader2, FlaskConical, Copy, Check, Download, FolderOpen } from "lucide-react"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism"
import api, { TestCase, PyTestGenerateResponse } from "@/services/api"

export function PyTestPage() {
  const [testCases, setTestCases] = useState<TestCase[]>([])
  const [requirement, setRequirement] = useState("")
  const [outputPath, setOutputPath] = useState("./tests")
  const [moduleName, setModuleName] = useState("test_generated")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<PyTestGenerateResponse | null>(null)
  const [copied, setCopied] = useState(false)
  const [mode, setMode] = useState<"testcases" | "requirement">("testcases")

  // Load test cases from session storage (from TestCasesPage)
  useEffect(() => {
    const storedTestCases = sessionStorage.getItem("testCases")
    if (storedTestCases) {
      try {
        const parsed = JSON.parse(storedTestCases)
        setTestCases(parsed)
        setMode("testcases")
      } catch {
        // Ignore parse errors
      }
    }
  }, [])

  const handleGenerateFromTestCases = async () => {
    if (testCases.length === 0) {
      setError("No test cases available. Generate test cases first or enter a requirement.")
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await api.generatePyTest({
        test_cases: testCases.map(tc => ({
          id: tc.id,
          title: tc.title,
          description: tc.description,
          preconditions: tc.preconditions,
          steps: tc.steps,
          expected_result: tc.expected_result,
          priority: tc.priority,
          test_type: tc.test_type,
        })),
        module_name: moduleName,
        output_path: outputPath,
        include_fixtures: true,
      })
      setResult(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate pytest code")
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateFromRequirement = async () => {
    if (!requirement.trim()) {
      setError("Please enter a requirement")
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await api.generatePyTestFromRequirement(
        requirement,
        undefined,
        outputPath,
        moduleName
      )
      setResult(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate pytest code")
    } finally {
      setLoading(false)
    }
  }

  const copyCode = async () => {
    if (result?.code) {
      await navigator.clipboard.writeText(result.code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const downloadCode = () => {
    if (result?.code) {
      const blob = new Blob([result.code], { type: "text/plain" })
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `${result.module_name}.py`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">PyTest Generator</h1>
        <p className="text-muted-foreground mt-2">
          Generate runnable pytest code from test cases or requirements
        </p>
      </div>

      {/* Mode Toggle */}
      <div className="flex gap-2">
        <Button
          variant={mode === "testcases" ? "default" : "outline"}
          onClick={() => setMode("testcases")}
        >
          From Test Cases
          {testCases.length > 0 && (
            <Badge variant="secondary" className="ml-2">
              {testCases.length}
            </Badge>
          )}
        </Button>
        <Button
          variant={mode === "requirement" ? "default" : "outline"}
          onClick={() => setMode("requirement")}
        >
          From Requirement
        </Button>
      </div>

      {/* Input Card */}
      <Card>
        <CardHeader>
          <CardTitle>
            {mode === "testcases" ? "Test Cases Input" : "Requirement Input"}
          </CardTitle>
          <CardDescription>
            {mode === "testcases"
              ? "Generate pytest code from structured test cases"
              : "Generate pytest code directly from a requirement description"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {mode === "testcases" ? (
            <>
              {testCases.length > 0 ? (
                <div className="space-y-2">
                  <label className="text-sm font-medium">
                    Loaded Test Cases ({testCases.length})
                  </label>
                  <div className="bg-muted p-3 rounded-md max-h-[200px] overflow-y-auto">
                    {testCases.map((tc, i) => (
                      <div key={tc.id} className="text-sm py-1 border-b last:border-0">
                        <span className="font-mono text-muted-foreground">{tc.id}</span>
                        {" - "}
                        <span>{tc.title}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <p>No test cases loaded.</p>
                  <p className="text-sm mt-1">
                    Go to Test Cases page to generate some, or switch to "From Requirement" mode.
                  </p>
                </div>
              )}
            </>
          ) : (
            <div>
              <label className="text-sm font-medium mb-2 block">
                Requirement <span className="text-destructive">*</span>
              </label>
              <Textarea
                placeholder="e.g., Test the user authentication flow including login, logout, and password reset functionality."
                value={requirement}
                onChange={(e) => setRequirement(e.target.value)}
                className="min-h-[120px]"
              />
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Module Name</label>
              <Input
                placeholder="test_generated"
                value={moduleName}
                onChange={(e) => setModuleName(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-2 block">
                Output Path
                <span className="text-muted-foreground font-normal ml-1">(auto-saves)</span>
              </label>
              <div className="flex gap-2">
                <Input
                  placeholder="./tests"
                  value={outputPath}
                  onChange={(e) => setOutputPath(e.target.value)}
                />
                <Button variant="outline" size="icon" title="Browse (coming soon)" disabled>
                  <FolderOpen className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>

          {error && (
            <div className="text-sm text-destructive bg-destructive/10 p-3 rounded-md">
              {error}
            </div>
          )}

          <Button
            onClick={
              mode === "testcases"
                ? handleGenerateFromTestCases
                : handleGenerateFromRequirement
            }
            disabled={loading || (mode === "testcases" && testCases.length === 0)}
            className="w-full"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <FlaskConical className="mr-2 h-4 w-4" />
                Generate PyTest Code
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Results */}
      {result && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Generated Code</CardTitle>
                <CardDescription>
                  {result.test_count} test functions in {result.module_name}.py
                  {result.saved_to && (
                    <span className="block mt-1 text-green-600">
                      ✓ Saved to: {result.saved_to}
                    </span>
                  )}
                </CardDescription>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={copyCode}>
                  {copied ? (
                    <>
                      <Check className="mr-2 h-4 w-4 text-green-500" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="mr-2 h-4 w-4" />
                      Copy
                    </>
                  )}
                </Button>
                <Button variant="outline" size="sm" onClick={downloadCode}>
                  <Download className="mr-2 h-4 w-4" />
                  Download
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg overflow-hidden border">
              <SyntaxHighlighter
                language="python"
                style={oneDark}
                customStyle={{
                  margin: 0,
                  borderRadius: 0,
                  fontSize: "13px",
                }}
                showLineNumbers
              >
                {result.code}
              </SyntaxHighlighter>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
