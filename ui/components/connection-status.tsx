"use client"

import { Wifi } from "lucide-react"

export function ConnectionStatus() {
  return (
    <div className="flex items-center gap-2">
      <Wifi className="h-4 w-4 text-green-500" />
      <span className="text-sm text-muted-foreground">Connected</span>
    </div>
  )
}
