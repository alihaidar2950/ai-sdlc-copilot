import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Github, GitPullRequest, FolderGit2 } from "lucide-react"

export function GitHubPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">GitHub Integration</h1>
        <p className="text-muted-foreground mt-2">
          Connect to GitHub repositories for automated test generation
        </p>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <CardTitle>Coming Soon</CardTitle>
            <Badge variant="secondary">In Development</Badge>
          </div>
          <CardDescription>
            GitHub integration is currently being developed
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="flex items-start gap-3 p-4 rounded-lg bg-muted/50">
              <FolderGit2 className="h-6 w-6 text-primary mt-1" />
              <div>
                <h3 className="font-medium">Repository Browser</h3>
                <p className="text-sm text-muted-foreground">
                  Browse and select files from any GitHub repository
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-4 rounded-lg bg-muted/50">
              <Github className="h-6 w-6 text-primary mt-1" />
              <div>
                <h3 className="font-medium">Auto-Analysis</h3>
                <p className="text-sm text-muted-foreground">
                  Automatically analyze code structure and generate tests
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-4 rounded-lg bg-muted/50">
              <GitPullRequest className="h-6 w-6 text-primary mt-1" />
              <div>
                <h3 className="font-medium">PR Creation</h3>
                <p className="text-sm text-muted-foreground">
                  Create pull requests with generated tests automatically
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
