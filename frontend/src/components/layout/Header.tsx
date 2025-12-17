import { useEffect, useState } from "react"
import { Badge } from "@/components/ui/badge"
import api from "@/services/api"

export function Header() {
  const [status, setStatus] = useState<"connected" | "disconnected" | "loading">(
    "loading"
  )

  useEffect(() => {
    const checkStatus = async () => {
      try {
        await api.getStatus()
        setStatus("connected")
      } catch {
        setStatus("disconnected")
      }
    }

    checkStatus()
    const interval = setInterval(checkStatus, 30000) // Check every 30s
    return () => clearInterval(interval)
  }, [])

  return (
    <header className="flex h-16 items-center justify-between border-b bg-card px-6">
      <div>
        <h1 className="text-xl font-semibold">AI SDLC Co-Pilot</h1>
        <p className="text-sm text-muted-foreground">
          Automated test case generation & code review
        </p>
      </div>

      <div className="flex items-center gap-4">
        <Badge
          variant={
            status === "connected"
              ? "success"
              : status === "disconnected"
              ? "destructive"
              : "secondary"
          }
        >
          {status === "connected"
            ? "🟢 Backend Connected"
            : status === "disconnected"
            ? "🔴 Backend Offline"
            : "⏳ Checking..."}
        </Badge>
      </div>
    </header>
  )
}
