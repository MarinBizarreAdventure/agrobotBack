"use client";

import { useState, useEffect } from "react"; // Added useEffect for potential dynamic data loading
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import {
  TrendingUp,
  TrendingDown,
  CalendarIcon,
  Download,
  Activity,
  Clock,
  MapPin,
  Zap,
  AlertTriangle,
  CheckCircle,
} from "lucide-react";
import { format } from "date-fns";

// Import mock data
import {
  moldovaRobots,
  moldovaFields,
  moldovaMissions,
} from "@/lib/mock/moldova-data";
import { mockAlerts } from "@/lib/mock/alerts";
import type { Robot, Field, Mission as MissionType, Alert } from "@/lib/types"; // Assuming Mission is named MissionType in types

// Helper to get the primary robot, field, and mission
const mainRobot =
  moldovaRobots.find((r) => r.id === "agrobot-01") || moldovaRobots[0];
const mainField =
  moldovaFields.find((f) => f.id === "field-a7") || moldovaFields[0];
const mainMission = mainRobot
  ? moldovaMissions.find(
      (m) => m.assignedRobot === mainRobot.id && m.status === "active"
    ) || moldovaMissions.find((m) => m.assignedRobot === mainRobot.id)
  : moldovaMissions[0];

// Process imported mock data for the dashboard
const performanceData = mainMission
  ? [
      {
        date: mainMission.startedAt || new Date().toISOString(),
        missions: 1,
        efficiency: mainMission.progress,
        uptime:
          mainRobot?.id === "agrobot-01"
            ? 10 // Low uptime for degraded agrobot-01 in chart
            : mainRobot?.telemetry?.system?.uptime
            ? (
                (mainRobot.telemetry.system.uptime / (24 * 60 * 60)) *
                100
              ).toFixed(1)
            : 95,
        coverage: mainField?.area || 0,
      },
      // Add a few more dummy points for trend illustration if needed, or keep it simple
      {
        date: new Date(
          Date.parse(mainMission.startedAt || new Date().toISOString()) -
            86400000 // Previous day
        ).toISOString(),
        missions: 1, // Assuming one mission for simplicity
        efficiency: 100, // Assuming full efficiency for a completed past mission
        uptime: mainRobot?.id === "agrobot-01" ? 12 : 96, // Slightly different low uptime for trend
        coverage: mainField?.area || 0,
      },
    ]
  : [];

const robotUtilization = mainRobot
  ? [
      {
        robot: mainRobot.name,
        active: mainRobot.status === "active" ? 100 : 0,
        idle: mainRobot.status === "idle" ? 100 : 0,
        maintenance:
          mainRobot.status === "warning" ||
          mainRobot.status === "offline" ||
          mainRobot.status === "unknown"
            ? 100
            : 0,
      },
    ]
  : [];

const missionTypesData = mainMission
  ? [
      {
        name:
          mainMission.type.charAt(0).toUpperCase() + mainMission.type.slice(1),
        value: 1,
        color: "#22c55e",
      },
    ]
  : [];

const fieldCoverageData = mainField
  ? [
      {
        field: mainField.name,
        coverage: mainField.coverage,
        area: mainField.area,
        missions: mainField.missions.length,
      },
    ]
  : [];

const alertsSummaryData = mockAlerts.reduce((acc, alert) => {
  const existing = acc.find((a) => a.type === alert.title); // Group by title for more specific alert types
  if (existing) {
    existing.count += 1;
  } else {
    acc.push({ type: alert.title, count: 1, severity: alert.severity });
  }
  return acc;
}, [] as { type: string; count: number; severity: string }[]);

export function AnalyticsDashboard() {
  const [dateRange, setDateRange] = useState<Date | undefined>(new Date());
  const [timeRange, setTimeRange] = useState("7d");

  // KPI Card Values
  const totalMissionsKPI = mainRobot?.totalMissions || 0;
  const avgEfficiencyKPI = mainMission?.progress || 0; // Using progress as a proxy for current mission efficiency

  let fleetUptimeKPI = "N/A";
  if (mainRobot?.uptime) {
    fleetUptimeKPI = mainRobot.uptime; // This is a string like "4h 23m"
  } else if (mainRobot?.telemetry?.system?.uptime) {
    const uptimeSeconds = mainRobot.telemetry.system.uptime;
    // Simple uptime percentage for the last 24h, assuming uptime is continuous for that period
    fleetUptimeKPI = `${(((uptimeSeconds % 86400) / 86400) * 100).toFixed(
      1
    )}% (today)`;
  }

  const areaCoveredKPI = mainField?.area || 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            Analytics Dashboard
          </h1>
          <p className="text-muted-foreground">
            Insights for {mainRobot?.name || "your fleet"}
          </p>
        </div>
        <div className="flex gap-2">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="24h">Last 24h</SelectItem>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 90 days</SelectItem>
            </SelectContent>
          </Select>
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="outline">
                <CalendarIcon className="h-4 w-4 mr-2" />
                {dateRange ? format(dateRange, "PPP") : "Pick a date"}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                mode="single"
                selected={dateRange}
                onSelect={setDateRange}
                initialFocus
              />
            </PopoverContent>
          </Popover>
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total Missions
            </CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalMissionsKPI}</div>
            <p className="text-xs text-muted-foreground flex items-center">
              {/* Static example, replace if dynamic trend is available */}
              <TrendingUp className="h-3 w-3 mr-1 text-green-500" />
              +5 from last period
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Avg Efficiency
            </CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{avgEfficiencyKPI}%</div>
            <p className="text-xs text-muted-foreground flex items-center">
              {/* Static example */}
              <TrendingUp className="h-3 w-3 mr-1 text-green-500" />
              +2% from last period
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Robot Uptime</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{fleetUptimeKPI}</div>
            <p className="text-xs text-muted-foreground flex items-center">
              {/* Static example */}
              <TrendingDown className="h-3 w-3 mr-1 text-red-500" />
              -1% from last period
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Area Covered</CardTitle>
            <MapPin className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{areaCoveredKPI} ha</div>
            <p className="text-xs text-muted-foreground flex items-center">
              {/* Static example */}
              <TrendingUp className="h-3 w-3 mr-1 text-green-500" />
              +10 ha from last period
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="performance" className="space-y-4">
        <TabsList>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="utilization">Robot Utilization</TabsTrigger>
          <TabsTrigger value="missions">Mission Analysis</TabsTrigger>
          <TabsTrigger value="fields">Field Coverage</TabsTrigger>
          <TabsTrigger value="alerts">Alerts & Issues</TabsTrigger>
        </TabsList>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Mission Performance Trends</CardTitle>
                <CardDescription>
                  Daily mission completion and efficiency metrics
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={performanceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis
                        dataKey="date"
                        tickFormatter={(value) =>
                          value ? format(new Date(value), "MMM dd") : ""
                        }
                      />
                      <YAxis />
                      <Tooltip
                        labelFormatter={(value) =>
                          value ? format(new Date(value), "PPP") : ""
                        }
                      />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="missions"
                        stroke="#3b82f6"
                        name="Missions"
                      />
                      <Line
                        type="monotone"
                        dataKey="efficiency"
                        stroke="#22c55e"
                        name="Efficiency %"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Fleet Uptime & Coverage</CardTitle>
                <CardDescription>
                  System availability and field coverage over time
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={performanceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis
                        dataKey="date"
                        tickFormatter={(value) =>
                          value ? format(new Date(value), "MMM dd") : ""
                        }
                      />
                      <YAxis />
                      <Tooltip
                        labelFormatter={(value) =>
                          value ? format(new Date(value), "PPP") : ""
                        }
                      />
                      <Legend />
                      <Area
                        type="monotone"
                        dataKey="uptime"
                        stackId="1"
                        stroke="#f59e0b"
                        fill="#f59e0b"
                        name="Uptime %"
                      />
                      <Area
                        type="monotone"
                        dataKey="coverage"
                        stackId="2"
                        stroke="#8b5cf6"
                        fill="#8b5cf6"
                        name="Coverage (ha)"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="utilization" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Robot Utilization Breakdown</CardTitle>
              <CardDescription>
                Time distribution across different robot states
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={robotUtilization}
                    layout={
                      robotUtilization && robotUtilization.length > 1
                        ? "horizontal"
                        : "vertical"
                    }
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    {robotUtilization && robotUtilization.length > 1 ? (
                      <>
                        <XAxis type="number" />
                        <YAxis dataKey="robot" type="category" />
                      </>
                    ) : (
                      <>
                        <XAxis dataKey="robot" type="category" />
                        <YAxis type="number" />
                      </>
                    )}
                    <Tooltip />
                    <Legend />
                    <Bar
                      dataKey="active"
                      stackId="a"
                      fill="#22c55e"
                      name="Active %"
                    />
                    <Bar
                      dataKey="idle"
                      stackId="a"
                      fill="#eab308"
                      name="Idle %"
                    />
                    <Bar
                      dataKey="maintenance"
                      stackId="a"
                      fill="#ef4444"
                      name="Maintenance %"
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="missions" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Mission Type Distribution</CardTitle>
                <CardDescription>
                  Breakdown of mission types over the selected period
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={missionTypesData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={100}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {missionTypesData.map((entry, index) => (
                          <Cell
                            key={`cell-${index}`}
                            fill={entry.color || "#8884d8"}
                          /> // Added fallback color
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Mission Success Rate</CardTitle>
                <CardDescription>
                  Success rate trends and completion statistics
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-500">
                      {mainMission && mainMission.status === "completed"
                        ? "100%"
                        : (mainMission?.progress || 0) + "%"}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {mainMission && mainMission.status === "completed"
                        ? "Success Rate"
                        : "Current Progress"}
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-500">
                      {mainRobot?.totalMissions || 0}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Completed
                    </div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Successful</span>
                    <span>147 missions</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-green-500 h-2 rounded-full"
                      style={{ width: "94.2%" }}
                    ></div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Failed</span>
                    <span>9 missions</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-red-500 h-2 rounded-full"
                      style={{ width: "5.8%" }}
                    ></div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="fields" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Field Coverage Analysis</CardTitle>
              <CardDescription>
                Coverage statistics and mission distribution across different
                fields
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {fieldCoverageData.map((field) => (
                  <div key={field.field} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{field.field}</span>
                        <Badge variant="outline">{field.area} ha</Badge>
                        <Badge variant="secondary">
                          {field.missions} missions
                        </Badge>
                      </div>
                      <span className="text-sm font-medium">
                        {field.coverage}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${field.coverage}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="alerts" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Alert Summary</CardTitle>
                <CardDescription>
                  Recent alerts and system notifications
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {alertsSummaryData.map((alert) => (
                  <div
                    key={alert.type}
                    className="flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2">
                      {alert.severity === "error" && (
                        <AlertTriangle className="h-4 w-4 text-red-500" />
                      )}
                      {alert.severity === "warning" && (
                        <AlertTriangle className="h-4 w-4 text-yellow-500" />
                      )}
                      {alert.severity === "info" && (
                        <CheckCircle className="h-4 w-4 text-blue-500" />
                      )}{" "}
                      {/* Changed from success to info for variety */}
                      {/* Add other severities if needed */}
                      <span className="font-medium">{alert.type}</span>
                    </div>
                    <Badge
                      variant={
                        alert.severity === "error"
                          ? "destructive"
                          : alert.severity === "warning"
                          ? "secondary"
                          : "default"
                      }
                    >
                      {alert.count}
                    </Badge>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>System Health Score</CardTitle>
                <CardDescription>
                  Overall fleet health and performance indicators
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-500">
                    {mainRobot
                      ? (
                          (mainRobot.components.filter(
                            (c) => c.status === "online"
                          ).length /
                            mainRobot.components.length) *
                          100
                        ).toFixed(0)
                      : "N/A"}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Health Score
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Robot Performance</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-500 h-2 rounded-full"
                          style={{
                            width: `${
                              mainRobot?.health || avgEfficiencyKPI || 0
                            }%`,
                          }}
                        ></div>{" "}
                        {/* Using robot health or efficiency */}
                      </div>
                      <span className="text-sm">
                        {mainRobot?.health || avgEfficiencyKPI || 0}%
                      </span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Communication</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-500 h-2 rounded-full"
                          style={{
                            width: `${
                              mainRobot?.telemetry?.communication
                                ?.signalStrength || 0
                            }%`,
                          }}
                        ></div>
                      </div>
                      <span className="text-sm">
                        {mainRobot?.telemetry?.communication?.signalStrength ||
                          0}
                        %
                      </span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Sensor Status</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-500 h-2 rounded-full"
                          style={{
                            width: `${
                              mainRobot
                                ? (
                                    (mainRobot.components.filter(
                                      (c) =>
                                        c.status === "online" &&
                                        (c.type === "gps" ||
                                          c.type === "camera")
                                    ).length /
                                      mainRobot.components.filter(
                                        (c) =>
                                          c.type === "gps" ||
                                          c.type === "camera"
                                      ).length) *
                                    100
                                  ).toFixed(0)
                                : 0
                            }%`,
                          }}
                        ></div>
                      </div>
                      <span className="text-sm">
                        {mainRobot
                          ? (
                              (mainRobot.components.filter(
                                (c) =>
                                  c.status === "online" &&
                                  (c.type === "gps" || c.type === "camera")
                              ).length /
                                mainRobot.components.filter(
                                  (c) => c.type === "gps" || c.type === "camera"
                                ).length) *
                              100
                            ).toFixed(0)
                          : 0}
                        %
                      </span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
