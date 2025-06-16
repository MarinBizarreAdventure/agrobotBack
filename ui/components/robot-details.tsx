"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Battery,
  Clock,
  Activity,
  AlertTriangle,
  CheckCircle,
  Pause,
  Square,
  Home,
  Settings,
  ArrowLeft,
  Navigation,
  Thermometer,
  Cpu,
  HardDrive,
  Wifi,
} from "lucide-react"
import Link from "next/link"
import { moldovaRobots } from "@/lib/mock/moldova-data"
import { TelemetryChart } from "@/components/telemetry-chart"
import { LeafletMap } from "@/components/leaflet-map"

interface RobotDetailsProps {
  robotId: string
}

export function RobotDetails({ robotId }: RobotDetailsProps) {
  const robot = moldovaRobots.find((r) => r.id === robotId)
  const [selectedTab, setSelectedTab] = useState("overview")

  if (!robot) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Link href="/fleet">
            <Button variant="outline" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Fleet
            </Button>
          </Link>
        </div>
        <Card>
          <CardContent className="p-6">
            <div className="text-center">
              <h2 className="text-xl font-semibold mb-2">Robot Not Found</h2>
              <p className="text-muted-foreground">The robot with ID "{robotId}" could not be found.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-green-500"
      case "idle":
        return "bg-yellow-500"
      case "warning":
        return "bg-orange-500"
      case "offline":
        return "bg-red-500"
      default:
        return "bg-gray-500"
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "active":
        return <Badge className="bg-green-500">Active</Badge>
      case "idle":
        return <Badge variant="secondary">Idle</Badge>
      case "warning":
        return <Badge variant="destructive">Warning</Badge>
      case "offline":
        return <Badge variant="outline">Offline</Badge>
      default:
        return <Badge variant="outline">Unknown</Badge>
    }
  }

  // Mock component health data
  const componentHealth = [
    { name: "Main Motor", status: "healthy", health: 95, temperature: 42 },
    { name: "GPS Module", status: "healthy", health: 98, temperature: 35 },
    { name: "Camera System", status: "warning", health: 87, temperature: 48 },
    { name: "Pixhawk Controller", status: "healthy", health: 92, temperature: 45 },
    { name: "Radio Module", status: "warning", health: 78, temperature: 52 },
    { name: "Battery Pack", status: "healthy", health: 85, temperature: 38 },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/fleet">
            <Button variant="outline" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Fleet
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{robot.name}</h1>
            <p className="text-muted-foreground">
              {robot.id} • {robot.type}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {getStatusBadge(robot.status)}
          <Button variant="outline">
            <Settings className="h-4 w-4 mr-2" />
            Configure
          </Button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Battery Level</CardTitle>
            <Battery className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{robot.battery}%</div>
            <Progress value={robot.battery} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Current Speed</CardTitle>
            <Navigation className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{robot.speed} m/s</div>
            <p className="text-xs text-muted-foreground">Heading: {robot.heading}°</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Uptime</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{robot.uptime}</div>
            <p className="text-xs text-muted-foreground">Since last restart</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Missions</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{robot.totalMissions}</div>
            <p className="text-xs text-muted-foreground">Completed successfully</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs value={selectedTab} onValueChange={setSelectedTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="telemetry">Telemetry</TabsTrigger>
          <TabsTrigger value="components">Components</TabsTrigger>
          <TabsTrigger value="location">Location</TabsTrigger>
          <TabsTrigger value="missions">Mission History</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Current Mission</CardTitle>
                <CardDescription>Active mission details and progress</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="font-medium">{robot.mission}</div>
                  <div className="text-sm text-muted-foreground mt-1">
                    Started: 2 hours ago • Estimated completion: 1.5 hours
                  </div>
                </div>
                <Progress value={67} className="h-2" />
                <div className="text-sm text-muted-foreground">67% complete</div>
                <div className="flex gap-2">
                  <Button size="sm" variant="outline">
                    <Pause className="h-3 w-3 mr-1" />
                    Pause
                  </Button>
                  <Button size="sm" variant="outline">
                    <Square className="h-3 w-3 mr-1" />
                    Stop
                  </Button>
                  <Button size="sm" variant="outline">
                    <Home className="h-3 w-3 mr-1" />
                    Return Home
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Robot Capabilities</CardTitle>
                <CardDescription>Available sensors and functions</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-2">
                  {robot.capabilities.map((capability) => (
                    <Badge key={capability} variant="outline" className="justify-center">
                      {capability}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>System Health</CardTitle>
              <CardDescription>Overall robot health and component status</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-500">92%</div>
                  <div className="text-sm text-muted-foreground">Overall Health</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-500">6/6</div>
                  <div className="text-sm text-muted-foreground">Components Online</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-500">2</div>
                  <div className="text-sm text-muted-foreground">Warnings</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="telemetry" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Real-time Telemetry</CardTitle>
              <CardDescription>Live sensor data and system metrics</CardDescription>
            </CardHeader>
            <CardContent>
              <TelemetryChart robotId={robot.id} />
            </CardContent>
          </Card>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">CPU Usage</CardTitle>
                <Cpu className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">45%</div>
                <Progress value={45} className="mt-2" />
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Memory Usage</CardTitle>
                <HardDrive className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">67%</div>
                <Progress value={67} className="mt-2" />
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Temperature</CardTitle>
                <Thermometer className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">42°C</div>
                <p className="text-xs text-muted-foreground">Normal range</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Signal Strength</CardTitle>
                <Wifi className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">89%</div>
                <p className="text-xs text-muted-foreground">Excellent</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="components" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Component Health</CardTitle>
              <CardDescription>Individual component status and diagnostics</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {componentHealth.map((component) => (
                  <div key={component.name} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-2">
                        {component.status === "healthy" ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : (
                          <AlertTriangle className="h-4 w-4 text-orange-500" />
                        )}
                        <span className="font-medium">{component.name}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-sm text-muted-foreground">{component.temperature}°C</div>
                      <div className="flex items-center gap-2">
                        <Progress value={component.health} className="w-20 h-2" />
                        <span className="text-sm font-medium">{component.health}%</span>
                      </div>
                      <Badge variant={component.status === "healthy" ? "default" : "secondary"}>
                        {component.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="location" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Current Location</CardTitle>
              <CardDescription>Real-time position and mission path</CardDescription>
            </CardHeader>
            <CardContent className="p-0">
              <div className="h-[500px] relative">
                <LeafletMap
                  robots={[robot]}
                  center={robot.position}
                  zoom={14}
                  selectedRobot={robot.id}
                  onRobotSelect={() => {}}
                  showMissions={true}
                  showFields={true}
                  className="rounded-b-lg"
                />
              </div>
            </CardContent>
          </Card>

          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Position Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Latitude:</span>
                  <span className="text-sm">{robot.position.lat.toFixed(6)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Longitude:</span>
                  <span className="text-sm">{robot.position.lng.toFixed(6)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Altitude:</span>
                  <span className="text-sm">{robot.position.altitude || 0}m</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Heading:</span>
                  <span className="text-sm">{robot.heading}°</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Speed:</span>
                  <span className="text-sm">{robot.speed} m/s</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>GPS Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Satellites:</span>
                  <span className="text-sm">12</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Accuracy:</span>
                  <span className="text-sm">1.2m</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Fix Type:</span>
                  <span className="text-sm">3D Fix</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm font-medium">Last Update:</span>
                  <span className="text-sm">2 seconds ago</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="missions" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Mission History</CardTitle>
              <CardDescription>Recent missions completed by this robot</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  {
                    id: "mission-001",
                    name: "Wheat Field Survey - Chișinău North",
                    status: "active",
                    progress: 67,
                    startTime: "2 hours ago",
                    estimatedCompletion: "1.5 hours",
                  },
                  {
                    id: "mission-045",
                    name: "Soil Analysis - Northern Sector",
                    status: "completed",
                    progress: 100,
                    startTime: "1 day ago",
                    completionTime: "3h 24m",
                  },
                  {
                    id: "mission-044",
                    name: "Crop Health Monitoring",
                    status: "completed",
                    progress: 100,
                    startTime: "2 days ago",
                    completionTime: "2h 15m",
                  },
                  {
                    id: "mission-043",
                    name: "Perimeter Inspection",
                    status: "completed",
                    progress: 100,
                    startTime: "3 days ago",
                    completionTime: "1h 45m",
                  },
                ].map((mission) => (
                  <div key={mission.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-3 h-3 rounded-full ${
                          mission.status === "active" ? "bg-green-500" : "bg-gray-400"
                        }`}
                      />
                      <div>
                        <div className="font-medium">{mission.name}</div>
                        <div className="text-sm text-muted-foreground">
                          Started: {mission.startTime}
                          {mission.status === "completed" && ` • Completed in: ${mission.completionTime}`}
                          {mission.status === "active" && ` • ETA: ${mission.estimatedCompletion}`}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2">
                        <Progress value={mission.progress} className="w-20 h-2" />
                        <span className="text-sm font-medium">{mission.progress}%</span>
                      </div>
                      <Badge variant={mission.status === "active" ? "default" : "secondary"}>{mission.status}</Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Emergency Controls */}
      <Card className="border-red-200 bg-red-50/50">
        <CardHeader>
          <CardTitle className="text-red-700">Emergency Controls</CardTitle>
          <CardDescription className="text-red-600">Use these controls only in emergency situations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Button variant="destructive" size="sm">
              <Square className="h-3 w-3 mr-1" />
              Emergency Stop
            </Button>
            <Button variant="outline" size="sm" className="border-red-200 text-red-700">
              <Home className="h-3 w-3 mr-1" />
              Force Return Home
            </Button>
            <Button variant="outline" size="sm" className="border-red-200 text-red-700">
              <AlertTriangle className="h-3 w-3 mr-1" />
              Cut Power
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
