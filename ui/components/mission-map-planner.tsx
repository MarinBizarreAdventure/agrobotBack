"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Trash2, RotateCcw, Save, Download } from "lucide-react"
import { LeafletMap } from "@/components/leaflet-map"
import { MOLDOVA_CENTER } from "@/lib/mock/moldova-data"

interface Waypoint {
  id: string
  lat: number
  lng: number
  altitude: number
  speed: number
  action: string
}

export function MissionMapPlanner() {
  const [waypoints, setWaypoints] = useState<Waypoint[]>([])
  const [selectedWaypoint, setSelectedWaypoint] = useState<string | null>(null)

  const clearWaypoints = () => {
    setWaypoints([])
    setSelectedWaypoint(null)
  }

  const removeSelectedWaypoint = () => {
    if (selectedWaypoint) {
      setWaypoints((prev) => prev.filter((wp) => wp.id !== selectedWaypoint))
      setSelectedWaypoint(null)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center gap-2">
          <Badge variant="outline">{waypoints.length} waypoints</Badge>
          {selectedWaypoint && (
            <Badge variant="secondary">WP{waypoints.findIndex((wp) => wp.id === selectedWaypoint) + 1} selected</Badge>
          )}
        </div>
        <div className="flex gap-2">
          <Button size="sm" variant="outline" onClick={removeSelectedWaypoint} disabled={!selectedWaypoint}>
            <Trash2 className="h-3 w-3" />
          </Button>
          <Button size="sm" variant="outline" onClick={clearWaypoints}>
            <RotateCcw className="h-3 w-3" />
          </Button>
          <Button size="sm" variant="outline">
            <Save className="h-3 w-3 mr-1" />
            Save
          </Button>
          <Button size="sm">
            <Download className="h-3 w-3 mr-1" />
            Export
          </Button>
        </div>
      </div>
      <div className="relative">
        <div className="h-[500px] relative">
          <LeafletMap
            robots={[]}
            center={MOLDOVA_CENTER}
            selectedRobot={null}
            onRobotSelect={() => {}}
            showMissions={false}
            showFields={true}
            className="rounded-lg"
          />
        </div>
        <div className="absolute top-2 left-2 bg-background/90 p-2 rounded text-xs">
          <div>Click on Moldova fields to add waypoints</div>
          <div>Click waypoint to select/deselect</div>
        </div>
      </div>
    </div>
  )
}
