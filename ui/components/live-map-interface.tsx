"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { MapPin, Navigation, Zap, Settings, Play, Pause, Home, RefreshCw } from "lucide-react"
import { LeafletMap } from "@/components/leaflet-map"
import { moldovaRobots, MOLDOVA_CENTER } from "@/lib/mock/moldova-data"

export function LiveMapInterface() {
  const [selectedRobot, setSelectedRobot] = useState<string | null>(null)
  const [mapCenter, setMapCenter] = useState(MOLDOVA_CENTER)

  const handleRobotSelect = (robotId: string) => {
    setSelectedRobot(robotId)
    const robot = moldovaRobots.find((r) => r.id === robotId)
    if (robot) {
      setMapCenter(robot.position)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "text-green-500"
      case "idle":
        return "text-yellow-500"
      case "warning":
        return "text-orange-500"
      case "offline":
        return "text-red-500"
      default:
        return "text-gray-500"
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Live Map - Moldova Agricultural Operations</h1>
          <p className="text-muted-foreground">Real-time robot tracking across Moldova's agricultural regions</p>
        </div>
        <Button variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      <div className="grid gap-4 lg:grid-cols-4">
        {/* Robot List Sidebar */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="h-5 w-5" />
              Active Robots
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {moldovaRobots.map((robot) => (
              <div
                key={robot.id}
                className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                  selectedRobot === robot.id ? "bg-accent" : "hover:bg-accent/50"
                }`}
                onClick={() => handleRobotSelect(robot.id)}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium">{robot.id}</span>
                  <Badge variant={robot.status === "active" ? "default" : "secondary"}>{robot.status}</Badge>
                </div>
                <div className="text-sm text-muted-foreground space-y-1">
                  <div className="flex items-center gap-2">
                    <Zap className="h-3 w-3" />
                    <span>{robot.battery}%</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Navigation className="h-3 w-3" />
                    <span>{robot.speed} m/s</span>
                  </div>
                  <div className="text-xs">{robot.mission}</div>
                </div>
                <div className="flex gap-1 mt-2">
                  <Button size="sm" variant="outline" className="h-6 px-2">
                    <Play className="h-3 w-3" />
                  </Button>
                  <Button size="sm" variant="outline" className="h-6 px-2">
                    <Pause className="h-3 w-3" />
                  </Button>
                  <Button size="sm" variant="outline" className="h-6 px-2">
                    <Home className="h-3 w-3" />
                  </Button>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Map Container */}
        <Card className="lg:col-span-3">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Moldova Agricultural Operations Map</CardTitle>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">
                  <Settings className="h-4 w-4 mr-2" />
                  Map Settings
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <div className="h-[600px] relative">
              <LeafletMap
                robots={moldovaRobots}
                center={mapCenter}
                selectedRobot={selectedRobot}
                onRobotSelect={setSelectedRobot}
                showMissions={true}
                showFields={true}
                className="rounded-b-lg"
              />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Selected Robot Details */}
      {selectedRobot && (
        <Card>
          <CardHeader>
            <CardTitle>Robot Details - {selectedRobot}</CardTitle>
          </CardHeader>
          <CardContent>
            {(() => {
              const robot = moldovaRobots.find((r) => r.id === selectedRobot)
              if (!robot) return null

              return (
                <div className="grid gap-4 md:grid-cols-4">
                  <div className="space-y-2">
                    <div className="text-sm font-medium">Status</div>
                    <Badge className={getStatusColor(robot.status)}>{robot.status.toUpperCase()}</Badge>
                  </div>
                  <div className="space-y-2">
                    <div className="text-sm font-medium">Battery Level</div>
                    <div className="text-2xl font-bold">{robot.battery}%</div>
                  </div>
                  <div className="space-y-2">
                    <div className="text-sm font-medium">Current Speed</div>
                    <div className="text-2xl font-bold">{robot.speed} m/s</div>
                  </div>
                  <div className="space-y-2">
                    <div className="text-sm font-medium">Heading</div>
                    <div className="text-2xl font-bold">{robot.heading}°</div>
                  </div>
                </div>
              )
            })()}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
