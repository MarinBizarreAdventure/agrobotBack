"use client"

import { useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Bot, MapPin, Battery, AlertTriangle, CheckCircle, Clock, TrendingUp } from "lucide-react"
import { FleetStatusChart } from "@/components/fleet-status-chart"
import { MissionProgressChart } from "@/components/mission-progress-chart"
import { RobotStatusCard } from "@/components/robot-status-card"
import { useRobotStore } from "@/lib/stores/robot.store"
import { useMissionStore } from "@/lib/stores/mission.store"
import { useAlertStore } from "@/lib/stores/alert.store"
import { formatRelativeTime } from "@/lib/utils/time"

export function DashboardOverview() {
  const { robots, loading: robotsLoading, fetchRobots } = useRobotStore()
  const { activeMissions, fetchMissions } = useMissionStore()
  const { alerts, unacknowledgedCount, fetchAlerts } = useAlertStore()

  useEffect(() => {
    fetchRobots()
    fetchMissions({ status: "active" })
    fetchAlerts({ acknowledged: false })
  }, [fetchRobots, fetchMissions, fetchAlerts])

  // Calculate fleet statistics
  const fleetStats = {
    totalRobots: robots.length,
    activeRobots: robots.filter((r) => r.status === "active").length,
    idleRobots: robots.filter((r) => r.status === "idle").length,
    offlineRobots: robots.filter((r) => r.status === "offline").length,
    activeMissions: activeMissions.length,
    completedToday: 12, // This would come from API
    totalFieldsCovered: 145.7, // This would come from API
    avgBatteryLevel: robots.length > 0 ? Math.round(robots.reduce((sum, r) => sum + r.battery, 0) / robots.length) : 0,
  }

  const recentAlerts = alerts.slice(0, 3).map((alert) => ({
    id: alert.id,
    robot: alert.robotId || "System",
    message: alert.message,
    severity: alert.severity,
    time: formatRelativeTime(alert.timestamp),
  }))

  const activeRobots = robots.filter((r) => r.status === "active" || r.status === "warning").slice(0, 3)

  if (robotsLoading) {
    return <div>Loading dashboard...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">Monitor your agricultural robot fleet in real-time</p>
      </div>

      {/* Stats Cards */}
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
            <CardTitle className="text-sm font-medium">Active Missions</CardTitle>
            <MapPin className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{fleetStats.activeMissions}</div>
            <p className="text-xs text-muted-foreground">{fleetStats.completedToday} completed today</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Field Coverage</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{fleetStats.totalFieldsCovered} ha</div>
            <p className="text-xs text-muted-foreground">+12.3% from last week</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Battery</CardTitle>
            <Battery className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{fleetStats.avgBatteryLevel}%</div>
            <Progress value={fleetStats.avgBatteryLevel} className="mt-2" />
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Fleet Status</CardTitle>
            <CardDescription>Real-time robot status distribution</CardDescription>
          </CardHeader>
          <CardContent>
            <FleetStatusChart robots={robots} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Mission Progress</CardTitle>
            <CardDescription>Daily mission completion trends</CardDescription>
          </CardHeader>
          <CardContent>
            <MissionProgressChart />
          </CardContent>
        </Card>
      </div>

      {/* Active Robots and Alerts */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Active Robots</CardTitle>
            <CardDescription>Currently deployed robots and their status</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {activeRobots.map((robot) => (
              <RobotStatusCard key={robot.id} robot={robot} />
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Alerts</CardTitle>
            <CardDescription>Latest system notifications and warnings</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentAlerts.map((alert) => (
              <div key={alert.id} className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  {alert.severity === "error" && <AlertTriangle className="h-5 w-5 text-red-500" />}
                  {alert.severity === "warning" && <AlertTriangle className="h-5 w-5 text-yellow-500" />}
                  {alert.severity === "info" && <CheckCircle className="h-5 w-5 text-green-500" />}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium">{alert.robot}</p>
                    <Badge
                      variant={
                        alert.severity === "error"
                          ? "destructive"
                          : alert.severity === "warning"
                            ? "secondary"
                            : "default"
                      }
                    >
                      {alert.severity}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{alert.message}</p>
                  <p className="text-xs text-muted-foreground flex items-center mt-1">
                    <Clock className="h-3 w-3 mr-1" />
                    {alert.time}
                  </p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
