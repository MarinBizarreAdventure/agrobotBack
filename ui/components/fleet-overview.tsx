"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import {
  Bot,
  Battery,
  MapPin,
  Clock,
  Activity,
  Search,
  MoreHorizontal,
  Play,
  Pause,
  Settings,
  ExternalLink,
} from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import Link from "next/link"
import { moldovaRobots } from "@/lib/mock/moldova-data"
import { TelemetryChart } from "@/components/telemetry-chart"

export function FleetOverview() {
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [selectedRobot, setSelectedRobot] = useState<string | null>(null)

  const filteredRobots = moldovaRobots.filter((robot) => {
    const matchesSearch =
      robot.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      robot.id.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "all" || robot.status === statusFilter
    return matchesSearch && matchesStatus
  })

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
      case "maintenance":
        return "bg-purple-500"
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
      case "maintenance":
        return <Badge className="bg-purple-500">Maintenance</Badge>
      default:
        return <Badge variant="outline">Unknown</Badge>
    }
  }

  const fleetStats = {
    totalRobots: moldovaRobots.length,
    activeRobots: moldovaRobots.filter((r) => r.status === "active").length,
    idleRobots: moldovaRobots.filter((r) => r.status === "idle").length,
    warningRobots: moldovaRobots.filter((r) => r.status === "warning").length,
    avgBattery: Math.round(moldovaRobots.reduce((sum, r) => sum + r.battery, 0) / moldovaRobots.length),
    totalMissions: moldovaRobots.reduce((sum, r) => sum + r.totalMissions, 0),
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Fleet Management</h1>
          <p className="text-muted-foreground">Monitor and control your agricultural robot fleet across Moldova</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Settings className="h-4 w-4 mr-2" />
            Fleet Settings
          </Button>
          <Button>
            <Bot className="h-4 w-4 mr-2" />
            Add Robot
          </Button>
        </div>
      </div>

      {/* Fleet Statistics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Robots</CardTitle>
            <Bot className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{fleetStats.totalRobots}</div>
            <p className="text-xs text-muted-foreground">
              {fleetStats.activeRobots} active, {fleetStats.idleRobots} idle
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Fleet Health</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {fleetStats.warningRobots === 0 ? (
                <span className="text-green-500">Healthy</span>
              ) : (
                <span className="text-orange-500">{fleetStats.warningRobots} Issues</span>
              )}
            </div>
            <p className="text-xs text-muted-foreground">
              {(((fleetStats.totalRobots - fleetStats.warningRobots) / fleetStats.totalRobots) * 100).toFixed(0)}%
              operational
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Battery</CardTitle>
            <Battery className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{fleetStats.avgBattery}%</div>
            <Progress value={fleetStats.avgBattery} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Missions</CardTitle>
            <MapPin className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{fleetStats.totalMissions}</div>
            <p className="text-xs text-muted-foreground">Completed missions</p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="robots" className="space-y-4">
        <TabsList>
          <TabsTrigger value="robots">Robot Fleet</TabsTrigger>
          <TabsTrigger value="telemetry">Fleet Telemetry</TabsTrigger>
          <TabsTrigger value="maintenance">Maintenance</TabsTrigger>
        </TabsList>

        <TabsContent value="robots" className="space-y-4">
          {/* Search and Filter */}
          <div className="flex gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search robots..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="idle">Idle</SelectItem>
                <SelectItem value="warning">Warning</SelectItem>
                <SelectItem value="offline">Offline</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Robot Grid */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {filteredRobots.map((robot) => (
              <Card key={robot.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(robot.status)}`} />
                      <div>
                        <CardTitle className="text-lg">{robot.name}</CardTitle>
                        <CardDescription>{robot.id}</CardDescription>
                      </div>
                    </div>
                    {getStatusBadge(robot.status)}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Robot Stats */}
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="flex items-center gap-2">
                      <Battery className="h-4 w-4" />
                      <span>{robot.battery}%</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="h-4 w-4" />
                      <span>{robot.uptime}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4" />
                      <span>{robot.speed} m/s</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Activity className="h-4 w-4" />
                      <span>{robot.totalMissions} missions</span>
                    </div>
                  </div>

                  {/* Current Mission */}
                  <div className="space-y-2">
                    <div className="text-sm font-medium">Current Mission</div>
                    <div className="text-sm text-muted-foreground">{robot.mission}</div>
                    {robot.status === "active" && <Progress value={Math.random() * 100} className="h-2" />}
                  </div>

                  {/* Robot Type and Capabilities */}
                  <div className="space-y-2">
                    <div className="text-sm font-medium">Type: {robot.type}</div>
                    <div className="flex flex-wrap gap-1">
                      {robot.capabilities.slice(0, 3).map((capability) => (
                        <Badge key={capability} variant="outline" className="text-xs">
                          {capability}
                        </Badge>
                      ))}
                      {robot.capabilities.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{robot.capabilities.length - 3}
                        </Badge>
                      )}
                    </div>
                  </div>

                  {/* Controls */}
                  <div className="flex gap-2 pt-2">
                    <Link href={`/fleet/${robot.id}`} className="flex-1">
                      <Button size="sm" variant="outline" className="w-full">
                        <ExternalLink className="h-3 w-3 mr-1" />
                        Details
                      </Button>
                    </Link>
                    <Button size="sm" variant="outline">
                      <Play className="h-3 w-3" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Pause className="h-3 w-3" />
                    </Button>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button size="sm" variant="outline">
                          <MoreHorizontal className="h-3 w-3" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent>
                        <DropdownMenuItem>Send to Location</DropdownMenuItem>
                        <DropdownMenuItem>Return Home</DropdownMenuItem>
                        <DropdownMenuItem>Schedule Maintenance</DropdownMenuItem>
                        <DropdownMenuItem className="text-red-600">Emergency Stop</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="telemetry" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            {moldovaRobots.slice(0, 4).map((robot) => (
              <Card key={robot.id}>
                <CardHeader>
                  <CardTitle className="text-lg">{robot.name}</CardTitle>
                  <CardDescription>Real-time telemetry data</CardDescription>
                </CardHeader>
                <CardContent>
                  <TelemetryChart robotId={robot.id} />
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="maintenance" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Maintenance Schedule</CardTitle>
              <CardDescription>Upcoming and overdue maintenance tasks</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {moldovaRobots.map((robot) => (
                  <div key={robot.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(robot.status)}`} />
                      <div>
                        <div className="font-medium">{robot.name}</div>
                        <div className="text-sm text-muted-foreground">
                          Last maintenance: {Math.floor(Math.random() * 30)} days ago
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={Math.random() > 0.7 ? "destructive" : "outline"}>
                        {Math.random() > 0.7 ? "Overdue" : "Scheduled"}
                      </Badge>
                      <Button size="sm" variant="outline">
                        Schedule
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
