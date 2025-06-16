"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { MapPin, Settings, Zap } from "lucide-react"

export function WaypointEditor() {
  const [missionSettings, setMissionSettings] = useState({
    name: "New Mission",
    type: "survey",
    altitude: 10,
    speed: 2,
    overlap: 20,
    pattern: "grid",
  })

  return (
    <div className="space-y-6">
      {/* Mission Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-4 w-4" />
            Mission Settings
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="mission-name">Mission Name</Label>
            <Input
              id="mission-name"
              value={missionSettings.name}
              onChange={(e) => setMissionSettings({ ...missionSettings, name: e.target.value })}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="mission-type">Mission Type</Label>
            <Select
              value={missionSettings.type}
              onValueChange={(value) => setMissionSettings({ ...missionSettings, type: value })}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="survey">Survey</SelectItem>
                <SelectItem value="monitoring">Monitoring</SelectItem>
                <SelectItem value="analysis">Analysis</SelectItem>
                <SelectItem value="inspection">Inspection</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="altitude">Altitude (m)</Label>
              <Input
                id="altitude"
                type="number"
                value={missionSettings.altitude}
                onChange={(e) => setMissionSettings({ ...missionSettings, altitude: Number(e.target.value) })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="speed">Speed (m/s)</Label>
              <Input
                id="speed"
                type="number"
                step="0.1"
                value={missionSettings.speed}
                onChange={(e) => setMissionSettings({ ...missionSettings, speed: Number(e.target.value) })}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Pattern Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-4 w-4" />
            Pattern Settings
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="pattern">Flight Pattern</Label>
            <Select
              value={missionSettings.pattern}
              onValueChange={(value) => setMissionSettings({ ...missionSettings, pattern: value })}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="grid">Grid Pattern</SelectItem>
                <SelectItem value="circular">Circular Pattern</SelectItem>
                <SelectItem value="linear">Linear Pattern</SelectItem>
                <SelectItem value="custom">Custom Path</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="overlap">Overlap (%)</Label>
            <Input
              id="overlap"
              type="number"
              value={missionSettings.overlap}
              onChange={(e) => setMissionSettings({ ...missionSettings, overlap: Number(e.target.value) })}
            />
          </div>
        </CardContent>
      </Card>

      {/* Mission Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-4 w-4" />
            Mission Summary
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div className="font-medium">Estimated Time</div>
              <div className="text-muted-foreground">2h 15m</div>
            </div>
            <div>
              <div className="font-medium">Distance</div>
              <div className="text-muted-foreground">4.2 km</div>
            </div>
            <div>
              <div className="font-medium">Area Coverage</div>
              <div className="text-muted-foreground">12.5 ha</div>
            </div>
            <div>
              <div className="font-medium">Battery Usage</div>
              <div className="text-muted-foreground">~65%</div>
            </div>
          </div>

          <Separator />

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Safety Checks</span>
              <Badge variant="outline" className="text-green-600">
                All Clear
              </Badge>
            </div>
            <div className="text-xs text-muted-foreground space-y-1">
              <div>✓ Within geofence boundaries</div>
              <div>✓ No-fly zones avoided</div>
              <div>✓ Weather conditions acceptable</div>
              <div>✓ Battery sufficient for mission</div>
            </div>
          </div>

          <div className="flex gap-2 pt-4">
            <Button className="flex-1">Deploy Mission</Button>
            <Button variant="outline">Save Draft</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
