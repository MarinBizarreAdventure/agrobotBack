"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
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
} from "recharts"
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
} from "lucide-react"
import { format } from "date-fns"

// Mock analytics data
const performanceData = [
  { date: "2024-01-01", missions: 12, efficiency: 87, uptime: 94, coverage: 145 },
  { date: "2024-01-02", missions: 15, efficiency: 92, uptime: 96, coverage: 178 },
  { date: "2024-01-03", missions: 8, efficiency: 78, uptime: 89, coverage: 98 },
  { date: "2024-01-04", missions: 18, efficiency: 95, uptime: 98, coverage: 203 },
  { date: "2024-01-05", missions: 14, efficiency: 89, uptime: 92, coverage: 167 },
  { date: "2024-01-06", missions: 16, efficiency: 91, uptime: 95, coverage: 189 },
  { date: "2024-01-07", missions: 11, efficiency: 85, uptime: 88, coverage: 134 },
]

const robotUtilization = [
  { robot: "AgroBot-01", active: 85, idle: 10, maintenance: 5 },
  { robot: "AgroBot-02", active: 78, idle: 15, maintenance: 7 },
  { robot: "AgroBot-03", active: 92, idle: 5, maintenance: 3 },
  { robot: "AgroBot-04", active: 67, idle: 25, maintenance: 8 },
]

const missionTypes = [
  { name: "Survey", value: 45, color: "#22c55e" },
  { name: "Monitoring", value: 30, color: "#3b82f6" },
  { name: "Analysis", value: 15, color: "#f59e0b" },
  { name: "Inspection", value: 10, color: "#ef4444" },
]

const fieldCoverage = [
  { field: "Field A-7", coverage: 95, area: 25.4, missions: 12 },
  { field: "Field B-3", coverage: 87, area: 18.7, missions: 8 },
  { field: "Field C-1", coverage: 92, area: 31.2, missions: 15 },
  { field: "Field D-2", coverage: 78, area: 22.1, missions: 6 },
  { field: "Field E-5", coverage: 89, area: 28.9, missions: 10 },
]

const alertsData = [
  { type: "Battery Low", count: 23, severity: "warning" },
  { type: "GPS Signal Lost", count: 8, severity: "error" },
  { type: "Mission Complete", count: 156, severity: "success" },
  { type: "Weather Alert", count: 12, severity: "warning" },
  { type: "Maintenance Due", count: 4, severity: "info" },
]

export function AnalyticsDashboard() {
  const [dateRange, setDateRange] = useState<Date | undefined>(new Date())
  const [timeRange, setTimeRange] = useState("7d")

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Analytics Dashboard</h1>
          <p className="text-muted-foreground">Comprehensive insights into your agricultural robot fleet performance</p>
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
              <Calendar mode="single" selected={dateRange} onSelect={setDateRange} initialFocus />
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
            <CardTitle className="text-sm font-medium">Total Missions</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">94</div>
            <p className="text-xs text-muted-foreground flex items-center">
              <TrendingUp className="h-3 w-3 mr-1 text-green-500" />
              +12% from last week
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Efficiency</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">89.2%</div>
            <p className="text-xs text-muted-foreground flex items-center">
              <TrendingUp className="h-3 w-3 mr-1 text-green-500" />
              +3.2% from last week
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Fleet Uptime</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">93.4%</div>
            <p className="text-xs text-muted-foreground flex items-center">
              <TrendingDown className="h-3 w-3 mr-1 text-red-500" />
              -1.8% from last week
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Area Covered</CardTitle>
            <MapPin className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,314 ha</div>
            <p className="text-xs text-muted-foreground flex items-center">
              <TrendingUp className="h-3 w-3 mr-1 text-green-500" />
              +8.7% from last week
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
                <CardDescription>Daily mission completion and efficiency metrics</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={performanceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" tickFormatter={(value) => format(new Date(value), "MMM dd")} />
                      <YAxis />
                      <Tooltip labelFormatter={(value) => format(new Date(value), "PPP")} />
                      <Legend />
                      <Line type="monotone" dataKey="missions" stroke="#3b82f6" name="Missions" />
                      <Line type="monotone" dataKey="efficiency" stroke="#22c55e" name="Efficiency %" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Fleet Uptime & Coverage</CardTitle>
                <CardDescription>System availability and field coverage over time</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={performanceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" tickFormatter={(value) => format(new Date(value), "MMM dd")} />
                      <YAxis />
                      <Tooltip labelFormatter={(value) => format(new Date(value), "PPP")} />
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
              <CardDescription>Time distribution across different robot states</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={robotUtilization} layout="horizontal">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="robot" type="category" />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="active" stackId="a" fill="#22c55e" name="Active %" />
                    <Bar dataKey="idle" stackId="a" fill="#eab308" name="Idle %" />
                    <Bar dataKey="maintenance" stackId="a" fill="#ef4444" name="Maintenance %" />
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
                <CardDescription>Breakdown of mission types over the selected period</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={missionTypes}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={100}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {missionTypes.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
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
                <CardDescription>Success rate trends and completion statistics</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-500">94.2%</div>
                    <div className="text-sm text-muted-foreground">Success Rate</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-500">156</div>
                    <div className="text-sm text-muted-foreground">Completed</div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Successful</span>
                    <span>147 missions</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: "94.2%" }}></div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Failed</span>
                    <span>9 missions</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-red-500 h-2 rounded-full" style={{ width: "5.8%" }}></div>
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
              <CardDescription>Coverage statistics and mission distribution across different fields</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {fieldCoverage.map((field) => (
                  <div key={field.field} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{field.field}</span>
                        <Badge variant="outline">{field.area} ha</Badge>
                        <Badge variant="secondary">{field.missions} missions</Badge>
                      </div>
                      <span className="text-sm font-medium">{field.coverage}%</span>
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
                <CardDescription>Recent alerts and system notifications</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {alertsData.map((alert) => (
                  <div key={alert.type} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {alert.severity === "error" && <AlertTriangle className="h-4 w-4 text-red-500" />}
                      {alert.severity === "warning" && <AlertTriangle className="h-4 w-4 text-yellow-500" />}
                      {alert.severity === "success" && <CheckCircle className="h-4 w-4 text-green-500" />}
                      {alert.severity === "info" && <Activity className="h-4 w-4 text-blue-500" />}
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
                <CardDescription>Overall fleet health and performance indicators</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-500">87</div>
                  <div className="text-sm text-muted-foreground">Health Score</div>
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Robot Performance</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div className="bg-green-500 h-2 rounded-full" style={{ width: "92%" }}></div>
                      </div>
                      <span className="text-sm">92%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Communication</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div className="bg-green-500 h-2 rounded-full" style={{ width: "89%" }}></div>
                      </div>
                      <span className="text-sm">89%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Battery Health</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-500 h-2 rounded-full" style={{ width: "78%" }}></div>
                      </div>
                      <span className="text-sm">78%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Sensor Status</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div className="bg-green-500 h-2 rounded-full" style={{ width: "95%" }}></div>
                      </div>
                      <span className="text-sm">95%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
