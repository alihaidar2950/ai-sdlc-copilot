import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Code2, GitBranch, FileSearch } from "lucide-react"

export function AnalyzePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Code Analysis</h1>
        <p className="text-muted-foreground mt-2">
          Analyze your codebase to generate contextual, working tests
        </p>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <CardTitle>Coming Soon</CardTitle>
            <Badge variant="secondary">In Development</Badge>
          </div>
          <CardDescription>
            This feature is currently being developed
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="flex items-start gap-3 p-4 rounded-lg bg-muted/50">
              <Code2 className="h-6 w-6 text-primary mt-1" />
              <div>
                <h3 className="font-medium">AST Analysis</h3>
                <p className="text-sm text-muted-foreground">
                  Parse Python code to extract functions, classes, and dependencies
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-4 rounded-lg bg-muted/50">
              <GitBranch className="h-6 w-6 text-primary mt-1" />
              <div>
                <h3 className="font-medium">GitHub Integration</h3>
                <p className="text-sm text-muted-foreground">
                  Connect to repositories and analyze code directly
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-4 rounded-lg bg-muted/50">
              <FileSearch className="h-6 w-6 text-primary mt-1" />
              <div>
                <h3 className="font-medium">Contextual Tests</h3>
                <p className="text-sm text-muted-foreground">
                  Generate tests that actually test your code, not just mocks
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
