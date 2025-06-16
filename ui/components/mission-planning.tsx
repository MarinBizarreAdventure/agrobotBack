"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Progress } from "@/components/ui/progress"
import { Plus, Play, Pause, Square, Edit, Trash2, Copy, MapPin, Clock, Route, Calendar, Search } from "lucide-react"
import { MissionMapPlanner } from "@/components/mission-map-planner"
import { WaypointEditor } from "@/components/waypoint-editor"

// Mock mission data
const missions = [
  {
    id: "MISSION-001",
    name: "Field Survey Alpha",
    description: "Complete survey of northern field section A-7",
    status: "active",
    assignedRobot: "AgroBot-01",
    progress: 67,
    waypoints: 12,
    estimatedTime: "2h 30m",
    actualTime: "1h 45m",
    fieldArea: "Field A-7",
    priority: "high",
    createdAt: "2024-01-15T08:00:00Z",
    startedAt: "2024-01-15T09:15:00Z",
    type: "survey",
  },
  {
    id: "MISSION-002",
    name: "Crop Health Monitoring",
    description: "Monitor crop health in eastern sectors B-3 and B-4",
    status: "scheduled",
    assignedRobot: "AgroBot-02",
    progress: 0,
    waypoints: 8,
    estimatedTime: "1h 45m",
    actualTime: null,
    fieldArea: "Field B-3, B-4",
    priority: "medium",
    createdAt: "2024-01-15T10:30:00Z",
    startedAt: null,
    type: "monitoring",
  },
  {
    id: "MISSION-003",
    name: "Soil Analysis Grid",
    description: "Systematic soil sampling across grid pattern",
    status: "completed",
    assignedRobot: "AgroBot-03",
    progress: 100,
    waypoints: 16,
    estimatedTime: "3h 15m",
    actualTime: "3h 8m",
    fieldArea: "Field C-1",
    priority: "low",
    createdAt: "2024-01-14T14:00:00Z",
    startedAt: "2024-01-15T06:00:00Z",
    type: "analysis",
  },
  {
    id: "MISSION-004",
    name: "Perimeter Inspection",
    description: "Check field boundaries and fence integrity",
    status: "paused",
    assignedRobot: "AgroBot-01",
    progress: 34,
    waypoints: 6,
    estimatedTime: "1h 20m",
    actualTime: "28m",
    fieldArea: "All Perimeters",
    priority: "medium",
    createdAt: "2024-01-15T11:00:00Z",
    startedAt: "2024-01-15T12:30:00Z",
    type: "inspection",
  },
]

const missionTemplates = [
  {
    id: "template-1",
    name: "Grid Survey Pattern",
    description: "Systematic grid-based field survey",
    waypoints: 20,
    estimatedTime: "2h 45m",
    type: "survey",
  },
  {
    id: "template-2",
    name: "Perimeter Patrol",
    description: "Complete field boundary inspection",
    waypoints: 8,
    estimatedTime: "1h 30m",
    type: "inspection",
  },
  {
    id: "template-3",
    name: "Crop Row Monitoring",
    description: "Follow crop rows for health monitoring",
    waypoints: 12,
    estimatedTime: "2h 15m",
    type: "monitoring",
  },
]

export function MissionPlanning() {
  const [selectedMission, setSelectedMission] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [newMission, setNewMission] = useState({
    name: "",
    description: "",
    type: "survey",
    priority: "medium",
    assignedRobot: "",
    fieldArea: "",
  })

  const filteredMissions = missions.filter((mission) => {
    const matchesSearch =
      mission.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      mission.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "all" || mission.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-green-500"
      case "scheduled":
        return "bg-blue-500"
      case "completed":
        return "bg-gray-500"
      case "paused":
        return "bg-yellow-500"
      case "failed":
        return "bg-red-500"
      default:
        return "bg-gray-500"
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "active":
        return <Badge className="bg-green-500">Active</Badge>
      case "scheduled":
        return <Badge className="bg-blue-500">Scheduled</Badge>
      case "completed":
        return <Badge variant="secondary">Completed</Badge>
      case "paused":
        return <Badge className="bg-yellow-500">Paused</Badge>
      case "failed":
        return <Badge variant="destructive">Failed</Badge>
      default:
        return <Badge variant="outline">Unknown</Badge>
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "text-red-500"
      case "medium":
        return "text-yellow-500"
      case "low":
        return "text-green-500"
      default:
        return "text-gray-500"
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Mission Planning</h1>
          <p className="text-muted-foreground">Create, manage, and monitor agricultural robot missions</p>
        </div>
        <div className="flex gap-2">
          <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                New Mission
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>Create New Mission</DialogTitle>
                <DialogDescription>Plan a new mission for your agricultural robots</DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="mission-name">Mission Name</Label>
                    <Input
                      id="mission-name"
                      value={newMission.name}
                      onChange={(e) => setNewMission({ ...newMission, name: e.target.value })}
                      placeholder="Enter mission name"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="mission-type">Mission Type</Label>
                    <Select
                      value={newMission.type}
                      onValueChange={(value) => setNewMission({ ...newMission, type: value })}
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
                </div>
                <div className="space-y-2">
                  <Label htmlFor="mission-description">Description</Label>
                  <Textarea
                    id="mission-description"
                    value={newMission.description}
                    onChange={(e) => setNewMission({ ...newMission, description: e.target.value })}
                    placeholder="Describe the mission objectives"
                  />
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="mission-priority">Priority</Label>
                    <Select
                      value={newMission.priority}
                      onValueChange={(value) => setNewMission({ ...newMission, priority: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="high">High</SelectItem>
                        <SelectItem value="medium">Medium</SelectItem>
                        <SelectItem value="low">Low</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="assigned-robot">Assigned Robot</Label>
                    <Select
                      value={newMission.assignedRobot}
                      onValueChange={(value) => setNewMission({ ...newMission, assignedRobot: value })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select robot" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="AgroBot-01">AgroBot-01</SelectItem>
                        <SelectItem value="AgroBot-02">AgroBot-02</SelectItem>
                        <SelectItem value="AgroBot-03">AgroBot-03</SelectItem>
                        <SelectItem value="AgroBot-04">AgroBot-04</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="field-area">Field Area</Label>
                    <Input
                      id="field-area"
                      value={newMission.fieldArea}
                      onChange={(e) => setNewMission({ ...newMission, fieldArea: e.target.value })}
                      placeholder="e.g., Field A-7"
                    />
                  </div>
                </div>
              </div>
              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
                  Cancel
                </Button>
                <Button onClick={() => setShowCreateDialog(false)}>Create Mission</Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <Tabs defaultValue="missions" className="space-y-4">
        <TabsList>
          <TabsTrigger value="missions">Active Missions</TabsTrigger>
          <TabsTrigger value="templates">Mission Templates</TabsTrigger>
          <TabsTrigger value="planner">Mission Planner</TabsTrigger>
        </TabsList>

        <TabsContent value="missions" className="space-y-4">
          {/* Search and Filter */}
          <div className="flex gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search missions..."
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
                <SelectItem value="scheduled">Scheduled</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
                <SelectItem value="paused">Paused</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Mission List */}
          <div className="grid gap-4">
            {filteredMissions.map((mission) => (
              <Card key={mission.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(mission.status)}`} />
                      <div>
                        <CardTitle className="text-lg">{mission.name}</CardTitle>
                        <CardDescription>{mission.description}</CardDescription>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {getStatusBadge(mission.status)}
                      <Badge variant="outline" className={getPriorityColor(mission.priority)}>
                        {mission.priority.toUpperCase()}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Mission Details */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div className="flex items-center gap-2">
                      <Route className="h-4 w-4" />
                      <span>{mission.waypoints} waypoints</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="h-4 w-4" />
                      <span>{mission.estimatedTime}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4" />
                      <span>{mission.fieldArea}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4" />
                      <span>{new Date(mission.createdAt).toLocaleDateString()}</span>
                    </div>
                  </div>

                  {/* Progress */}
                  {mission.status === "active" && (
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span>Progress</span>
                        <span>{mission.progress}%</span>
                      </div>
                      <Progress value={mission.progress} className="h-2" />
                    </div>
                  )}

                  {/* Mission Info */}
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <span>Assigned to: {mission.assignedRobot}</span>
                    {mission.actualTime && <span>Actual time: {mission.actualTime}</span>}
                  </div>

                  {/* Controls */}
                  <div className="flex gap-2 pt-2">
                    {mission.status === "scheduled" && (
                      <Button size="sm" variant="outline">
                        <Play className="h-3 w-3 mr-1" />
                        Start
                      </Button>
                    )}
                    {mission.status === "active" && (
                      <Button size="sm" variant="outline">
                        <Pause className="h-3 w-3 mr-1" />
                        Pause
                      </Button>
                    )}
                    {mission.status === "paused" && (
                      <Button size="sm" variant="outline">
                        <Play className="h-3 w-3 mr-1" />
                        Resume
                      </Button>
                    )}
                    <Button size="sm" variant="outline">
                      <Edit className="h-3 w-3 mr-1" />
                      Edit
                    </Button>
                    <Button size="sm" variant="outline">
                      <Copy className="h-3 w-3 mr-1" />
                      Clone
                    </Button>
                    {mission.status !== "active" && (
                      <Button size="sm" variant="outline">
                        <Square className="h-3 w-3 mr-1" />
                        Stop
                      </Button>
                    )}
                    <Button size="sm" variant="outline" className="text-red-600">
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="templates" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {missionTemplates.map((template) => (
              <Card key={template.id} className="hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <CardTitle className="text-lg">{template.name}</CardTitle>
                  <CardDescription>{template.description}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <Route className="h-4 w-4" />
                      <span>{template.waypoints} waypoints</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="h-4 w-4" />
                      <span>{template.estimatedTime}</span>
                    </div>
                  </div>
                  <Badge variant="outline">{template.type}</Badge>
                  <div className="flex gap-2">
                    <Button size="sm" className="flex-1">
                      Use Template
                    </Button>
                    <Button size="sm" variant="outline">
                      <Edit className="h-3 w-3" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="planner" className="space-y-4">
          <div className="grid gap-4 lg:grid-cols-3">
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Mission Map Planner</CardTitle>
                <CardDescription>Click on the map to add waypoints and plan your mission route</CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                <MissionMapPlanner />
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Waypoint Editor</CardTitle>
                <CardDescription>Configure waypoints and mission parameters</CardDescription>
              </CardHeader>
              <CardContent>
                <WaypointEditor />
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
