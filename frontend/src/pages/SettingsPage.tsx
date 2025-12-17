import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Settings, Key, Server } from "lucide-react"

export function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground mt-2">
          Configure your AI SDLC Co-Pilot preferences
        </p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Server className="h-5 w-5" />
              <CardTitle>Backend Configuration</CardTitle>
            </div>
            <CardDescription>
              Configure the connection to the backend API
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">API Base URL</label>
              <Input
                placeholder="http://localhost:8000/api/v1"
                defaultValue="http://localhost:8000/api/v1"
                disabled
              />
              <p className="text-xs text-muted-foreground mt-1">
                Set via VITE_API_URL environment variable
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Key className="h-5 w-5" />
              <CardTitle>API Keys</CardTitle>
              <Badge variant="secondary">Coming Soon</Badge>
            </div>
            <CardDescription>
              Configure API keys for external services
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">GitHub Token</label>
              <Input
                type="password"
                placeholder="ghp_xxxxxxxxxxxx"
                disabled
              />
              <p className="text-xs text-muted-foreground mt-1">
                Required for private repositories and higher rate limits
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              <CardTitle>Generation Preferences</CardTitle>
              <Badge variant="secondary">Coming Soon</Badge>
            </div>
            <CardDescription>
              Customize how tests are generated
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Default Output Path</label>
              <Input
                placeholder="./tests"
                defaultValue="./tests"
                disabled
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-2 block">Default Test Framework</label>
              <Input
                placeholder="pytest"
                defaultValue="pytest"
                disabled
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
