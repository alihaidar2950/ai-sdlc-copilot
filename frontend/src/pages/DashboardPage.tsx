import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { FileText, FlaskConical, Code2, ArrowRight, CheckCircle, XCircle } from "lucide-react"
import api, { ApiStatus } from "@/services/api"

export function DashboardPage() {
  const [status, setStatus] = useState<ApiStatus | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api.getStatus()
      .then(setStatus)
      .catch(() => setError("Backend not reachable"))
  }, [])

  const features = [
    {
      title: "Test Case Generation",
      description: "Generate comprehensive test cases from requirements using AI",
      icon: FileText,
      href: "/testcases",
      status: "ready",
    },
    {
      title: "PyTest Generator",
      description: "Convert test cases into runnable pytest code",
      icon: FlaskConical,
      href: "/pytest",
      status: "ready",
    },
    {
      title: "Code Analysis",
      description: "Analyze your codebase to generate contextual tests",
      icon: Code2,
      href: "/analyze",
      status: "coming-soon",
    },
  ]

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Welcome to AI SDLC Co-Pilot</h1>
        <p className="text-muted-foreground mt-2">
          Automate your software testing lifecycle with AI-powered tools
        </p>
      </div>

      {/* Status Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            Backend Status
            {status ? (
              <Badge variant="success" className="ml-2">
                <CheckCircle className="h-3 w-3 mr-1" />
                Connected
              </Badge>
            ) : error ? (
              <Badge variant="destructive" className="ml-2">
                <XCircle className="h-3 w-3 mr-1" />
                Offline
              </Badge>
            ) : (
              <Badge variant="secondary" className="ml-2">Loading...</Badge>
            )}
          </CardTitle>
        </CardHeader>
        {status && (
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <p className="text-muted-foreground">App</p>
                <p className="font-medium">{status.app}</p>
              </div>
              <div>
                <p className="text-muted-foreground">Version</p>
                <p className="font-medium">{status.version}</p>
              </div>
              <div>
                <p className="text-muted-foreground">Environment</p>
                <p className="font-medium">{status.environment}</p>
              </div>
              <div>
                <p className="text-muted-foreground">Debug Mode</p>
                <p className="font-medium">{status.debug ? "Enabled" : "Disabled"}</p>
              </div>
            </div>
          </CardContent>
        )}
      </Card>

      {/* Feature Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {features.map((feature) => (
          <Card key={feature.title} className="relative overflow-hidden">
            <CardHeader>
              <div className="flex items-center justify-between">
                <feature.icon className="h-8 w-8 text-primary" />
                {feature.status === "coming-soon" && (
                  <Badge variant="secondary">Coming Soon</Badge>
                )}
              </div>
              <CardTitle className="mt-4">{feature.title}</CardTitle>
              <CardDescription>{feature.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <Button
                asChild
                variant={feature.status === "ready" ? "default" : "secondary"}
                disabled={feature.status !== "ready"}
                className="w-full"
              >
                <Link to={feature.href}>
                  Get Started
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Start Guide */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Start Guide</CardTitle>
          <CardDescription>Follow these steps to generate your first tests</CardDescription>
        </CardHeader>
        <CardContent>
          <ol className="list-decimal list-inside space-y-3 text-sm">
            <li className="text-muted-foreground">
              <span className="text-foreground font-medium">Enter your requirement</span> - Describe the feature you want to test in natural language
            </li>
            <li className="text-muted-foreground">
              <span className="text-foreground font-medium">Generate test cases</span> - AI will create comprehensive test scenarios
            </li>
            <li className="text-muted-foreground">
              <span className="text-foreground font-medium">Convert to pytest</span> - Transform test cases into runnable Python code
            </li>
            <li className="text-muted-foreground">
              <span className="text-foreground font-medium">Run your tests</span> - Execute the generated tests in your project
            </li>
          </ol>
        </CardContent>
      </Card>
    </div>
  )
}
