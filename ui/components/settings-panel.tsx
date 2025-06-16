"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { Settings, Wifi, Shield, Bell, Map, Bot, Save, RefreshCw, Server, Key, Users } from "lucide-react"

export function SettingsPanel() {
  const [settings, setSettings] = useState({
    // System Settings
    systemName: "AgroBot Control System",
    timezone: "UTC-5",
    language: "en",
    autoBackup: true,
    debugMode: false,

    // API Settings
    backendUrl: "http://localhost:5000",
    piControllerUrl: "http://192.168.1.100:8000",
    apiTimeout: 30,
    retryAttempts: 3,

    // Communication Settings
    mqttBroker: "mqtt://localhost:1883",
    mqttUsername: "agrobot",
    mqttPassword: "",
    websocketUrl: "ws://localhost:8080",
    heartbeatInterval: 30,

    // Map Settings
    mapProvider: "openstreetmap",
    defaultZoom: 15,
    showTrails: true,
    trailDuration: 24,
    refreshRate: 5,

    // Robot Settings
    defaultAltitude: 10,
    defaultSpeed: 2.0,
    safetyRadius: 50,
    batteryWarning: 25,
    batteryLow: 15,

    // Notifications
    emailNotifications: true,
    pushNotifications: true,
    soundAlerts: true,
    alertBattery: true,
    alertMission: true,
    alertSystem: true,

    // Security
    sessionTimeout: 60,
    requireAuth: true,
    twoFactorAuth: false,
    apiKeyRotation: 30,
  })

  const handleSettingChange = (key: string, value: any) => {
    setSettings((prev) => ({ ...prev, [key]: value }))
  }

  const saveSettings = () => {
    // In a real app, this would save to backend
    console.log("Saving settings:", settings)
  }

  const resetSettings = () => {
    // Reset to defaults
    console.log("Resetting settings to defaults")
  }

  const testConnection = (type: string) => {
    console.log(`Testing ${type} connection...`)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
          <p className="text-muted-foreground">Configure your AgroBot system preferences and connections</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={resetSettings}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Reset
          </Button>
          <Button onClick={saveSettings}>
            <Save className="h-4 w-4 mr-2" />
            Save Changes
          </Button>
        </div>
      </div>

      <Tabs defaultValue="system" className="space-y-4">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="system">System</TabsTrigger>
          <TabsTrigger value="api">API & Connections</TabsTrigger>
          <TabsTrigger value="robots">Robots</TabsTrigger>
          <TabsTrigger value="map">Map & Display</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
        </TabsList>

        <TabsContent value="system" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                System Configuration
              </CardTitle>
              <CardDescription>General system settings and preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="system-name">System Name</Label>
                  <Input
                    id="system-name"
                    value={settings.systemName}
                    onChange={(e) => handleSettingChange("systemName", e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="timezone">Timezone</Label>
                  <Select value={settings.timezone} onValueChange={(value) => handleSettingChange("timezone", value)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="UTC-8">UTC-8 (Pacific)</SelectItem>
                      <SelectItem value="UTC-7">UTC-7 (Mountain)</SelectItem>
                      <SelectItem value="UTC-6">UTC-6 (Central)</SelectItem>
                      <SelectItem value="UTC-5">UTC-5 (Eastern)</SelectItem>
                      <SelectItem value="UTC+0">UTC+0 (GMT)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="language">Language</Label>
                  <Select value={settings.language} onValueChange={(value) => handleSettingChange("language", value)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="en">English</SelectItem>
                      <SelectItem value="es">Spanish</SelectItem>
                      <SelectItem value="fr">French</SelectItem>
                      <SelectItem value="de">German</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Auto Backup</Label>
                    <div className="text-sm text-muted-foreground">Automatically backup system data daily</div>
                  </div>
                  <Switch
                    checked={settings.autoBackup}
                    onCheckedChange={(checked) => handleSettingChange("autoBackup", checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Debug Mode</Label>
                    <div className="text-sm text-muted-foreground">Enable detailed logging and diagnostics</div>
                  </div>
                  <Switch
                    checked={settings.debugMode}
                    onCheckedChange={(checked) => handleSettingChange("debugMode", checked)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="api" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Server className="h-5 w-5" />
                API Endpoints
              </CardTitle>
              <CardDescription>Configure backend API connections and settings</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="backend-url">Backend API URL</Label>
                  <div className="flex gap-2">
                    <Input
                      id="backend-url"
                      value={settings.backendUrl}
                      onChange={(e) => handleSettingChange("backendUrl", e.target.value)}
                      placeholder="http://localhost:5000"
                    />
                    <Button variant="outline" onClick={() => testConnection("backend")}>
                      Test
                    </Button>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="pi-controller-url">Pi Controller URL</Label>
                  <div className="flex gap-2">
                    <Input
                      id="pi-controller-url"
                      value={settings.piControllerUrl}
                      onChange={(e) => handleSettingChange("piControllerUrl", e.target.value)}
                      placeholder="http://192.168.1.100:8000"
                    />
                    <Button variant="outline" onClick={() => testConnection("pi-controller")}>
                      Test
                    </Button>
                  </div>
                </div>
              </div>

              <Separator />

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="api-timeout">API Timeout (seconds)</Label>
                  <Input
                    id="api-timeout"
                    type="number"
                    value={settings.apiTimeout}
                    onChange={(e) => handleSettingChange("apiTimeout", Number(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="retry-attempts">Retry Attempts</Label>
                  <Input
                    id="retry-attempts"
                    type="number"
                    value={settings.retryAttempts}
                    onChange={(e) => handleSettingChange("retryAttempts", Number(e.target.value))}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Wifi className="h-5 w-5" />
                Communication Settings
              </CardTitle>
              <CardDescription>Configure MQTT, WebSocket, and real-time communication</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="mqtt-broker">MQTT Broker URL</Label>
                  <div className="flex gap-2">
                    <Input
                      id="mqtt-broker"
                      value={settings.mqttBroker}
                      onChange={(e) => handleSettingChange("mqttBroker", e.target.value)}
                      placeholder="mqtt://localhost:1883"
                    />
                    <Button variant="outline" onClick={() => testConnection("mqtt")}>
                      Test
                    </Button>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="mqtt-username">MQTT Username</Label>
                    <Input
                      id="mqtt-username"
                      value={settings.mqttUsername}
                      onChange={(e) => handleSettingChange("mqttUsername", e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="mqtt-password">MQTT Password</Label>
                    <Input
                      id="mqtt-password"
                      type="password"
                      value={settings.mqttPassword}
                      onChange={(e) => handleSettingChange("mqttPassword", e.target.value)}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="websocket-url">WebSocket URL</Label>
                  <div className="flex gap-2">
                    <Input
                      id="websocket-url"
                      value={settings.websocketUrl}
                      onChange={(e) => handleSettingChange("websocketUrl", e.target.value)}
                      placeholder="ws://localhost:8080"
                    />
                    <Button variant="outline" onClick={() => testConnection("websocket")}>
                      Test
                    </Button>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="heartbeat-interval">Heartbeat Interval (seconds)</Label>
                  <Input
                    id="heartbeat-interval"
                    type="number"
                    value={settings.heartbeatInterval}
                    onChange={(e) => handleSettingChange("heartbeatInterval", Number(e.target.value))}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="robots" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bot className="h-5 w-5" />
                Robot Configuration
              </CardTitle>
              <CardDescription>Default settings and safety parameters for agricultural robots</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="default-altitude">Default Altitude (m)</Label>
                  <Input
                    id="default-altitude"
                    type="number"
                    value={settings.defaultAltitude}
                    onChange={(e) => handleSettingChange("defaultAltitude", Number(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="default-speed">Default Speed (m/s)</Label>
                  <Input
                    id="default-speed"
                    type="number"
                    step="0.1"
                    value={settings.defaultSpeed}
                    onChange={(e) => handleSettingChange("defaultSpeed", Number(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="safety-radius">Safety Radius (m)</Label>
                  <Input
                    id="safety-radius"
                    type="number"
                    value={settings.safetyRadius}
                    onChange={(e) => handleSettingChange("safetyRadius", Number(e.target.value))}
                  />
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <h4 className="font-medium">Battery Alert Thresholds</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="battery-warning">Warning Level (%)</Label>
                    <Input
                      id="battery-warning"
                      type="number"
                      value={settings.batteryWarning}
                      onChange={(e) => handleSettingChange("batteryWarning", Number(e.target.value))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="battery-low">Critical Level (%)</Label>
                    <Input
                      id="battery-low"
                      type="number"
                      value={settings.batteryLow}
                      onChange={(e) => handleSettingChange("batteryLow", Number(e.target.value))}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="map" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Map className="h-5 w-5" />
                Map & Display Settings
              </CardTitle>
              <CardDescription>Configure map provider, display options, and refresh rates</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="map-provider">Map Provider</Label>
                  <Select
                    value={settings.mapProvider}
                    onValueChange={(value) => handleSettingChange("mapProvider", value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="openstreetmap">OpenStreetMap</SelectItem>
                      <SelectItem value="google">Google Maps</SelectItem>
                      <SelectItem value="mapbox">Mapbox</SelectItem>
                      <SelectItem value="satellite">Satellite View</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="default-zoom">Default Zoom Level</Label>
                  <Input
                    id="default-zoom"
                    type="number"
                    min="1"
                    max="20"
                    value={settings.defaultZoom}
                    onChange={(e) => handleSettingChange("defaultZoom", Number(e.target.value))}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="trail-duration">Trail Duration (hours)</Label>
                  <Input
                    id="trail-duration"
                    type="number"
                    value={settings.trailDuration}
                    onChange={(e) => handleSettingChange("trailDuration", Number(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="refresh-rate">Refresh Rate (seconds)</Label>
                  <Input
                    id="refresh-rate"
                    type="number"
                    value={settings.refreshRate}
                    onChange={(e) => handleSettingChange("refreshRate", Number(e.target.value))}
                  />
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Show Robot Trails</Label>
                    <div className="text-sm text-muted-foreground">Display historical movement paths</div>
                  </div>
                  <Switch
                    checked={settings.showTrails}
                    onCheckedChange={(checked) => handleSettingChange("showTrails", checked)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Notification Preferences
              </CardTitle>
              <CardDescription>Configure how and when you receive system alerts</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Email Notifications</Label>
                    <div className="text-sm text-muted-foreground">Receive alerts via email</div>
                  </div>
                  <Switch
                    checked={settings.emailNotifications}
                    onCheckedChange={(checked) => handleSettingChange("emailNotifications", checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Push Notifications</Label>
                    <div className="text-sm text-muted-foreground">Browser push notifications</div>
                  </div>
                  <Switch
                    checked={settings.pushNotifications}
                    onCheckedChange={(checked) => handleSettingChange("pushNotifications", checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Sound Alerts</Label>
                    <div className="text-sm text-muted-foreground">Audio notifications for critical alerts</div>
                  </div>
                  <Switch
                    checked={settings.soundAlerts}
                    onCheckedChange={(checked) => handleSettingChange("soundAlerts", checked)}
                  />
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <h4 className="font-medium">Alert Types</h4>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Battery Alerts</Label>
                    <div className="text-sm text-muted-foreground">Low battery warnings</div>
                  </div>
                  <Switch
                    checked={settings.alertBattery}
                    onCheckedChange={(checked) => handleSettingChange("alertBattery", checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Mission Alerts</Label>
                    <div className="text-sm text-muted-foreground">Mission status updates</div>
                  </div>
                  <Switch
                    checked={settings.alertMission}
                    onCheckedChange={(checked) => handleSettingChange("alertMission", checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>System Alerts</Label>
                    <div className="text-sm text-muted-foreground">System errors and warnings</div>
                  </div>
                  <Switch
                    checked={settings.alertSystem}
                    onCheckedChange={(checked) => handleSettingChange("alertSystem", checked)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Security Settings
              </CardTitle>
              <CardDescription>Authentication, access control, and security preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="session-timeout">Session Timeout (minutes)</Label>
                  <Input
                    id="session-timeout"
                    type="number"
                    value={settings.sessionTimeout}
                    onChange={(e) => handleSettingChange("sessionTimeout", Number(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="api-key-rotation">API Key Rotation (days)</Label>
                  <Input
                    id="api-key-rotation"
                    type="number"
                    value={settings.apiKeyRotation}
                    onChange={(e) => handleSettingChange("apiKeyRotation", Number(e.target.value))}
                  />
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Require Authentication</Label>
                    <div className="text-sm text-muted-foreground">Require login to access system</div>
                  </div>
                  <Switch
                    checked={settings.requireAuth}
                    onCheckedChange={(checked) => handleSettingChange("requireAuth", checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Two-Factor Authentication</Label>
                    <div className="text-sm text-muted-foreground">Enable 2FA for enhanced security</div>
                  </div>
                  <Switch
                    checked={settings.twoFactorAuth}
                    onCheckedChange={(checked) => handleSettingChange("twoFactorAuth", checked)}
                  />
                </div>
              </div>

              <Separator />

              <div className="space-y-4">
                <h4 className="font-medium">API Keys</h4>
                <div className="space-y-2">
                  <Label>Current API Key</Label>
                  <div className="flex gap-2">
                    <Input value="ak_1234567890abcdef..." readOnly />
                    <Button variant="outline">
                      <Key className="h-4 w-4 mr-2" />
                      Regenerate
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Access Control
              </CardTitle>
              <CardDescription>Manage user permissions and access levels</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <div className="font-medium">Administrator</div>
                    <div className="text-sm text-muted-foreground">Full system access</div>
                  </div>
                  <Badge>Active</Badge>
                </div>
                <div className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <div className="font-medium">Operator</div>
                    <div className="text-sm text-muted-foreground">Mission control and monitoring</div>
                  </div>
                  <Badge variant="secondary">Inactive</Badge>
                </div>
                <div className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <div className="font-medium">Viewer</div>
                    <div className="text-sm text-muted-foreground">Read-only access</div>
                  </div>
                  <Badge variant="secondary">Inactive</Badge>
                </div>
              </div>
              <Button variant="outline" className="w-full">
                <Users className="h-4 w-4 mr-2" />
                Manage Users
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
