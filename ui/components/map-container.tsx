"use client"

import { useEffect, useRef, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { X, ExternalLink, Battery, Navigation, MapPin } from "lucide-react"

interface Robot {
  id: string
  position: { lat: number; lng: number }
  status: "active" | "idle" | "warning" | "offline"
  battery: number
  mission: string
  heading: number
  speed: number
}

interface MapContainerProps {
  robots: Robot[]
  center: { lat: number; lng: number }
  selectedRobot: string | null
  onRobotSelect: (robotId: string) => void
}

interface PopupState {
  robot: Robot | null
  x: number
  y: number
  visible: boolean
}

export function MapContainer({ robots, center, selectedRobot, onRobotSelect }: MapContainerProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [popup, setPopup] = useState<PopupState>({ robot: null, x: 0, y: 0, visible: false })
  const router = useRouter()

  // Mock mission paths for demonstration
  const missionPaths = {
    "AgroBot-01": [
      { lat: 40.7128, lng: -74.006 },
      { lat: 40.7138, lng: -74.005 },
      { lat: 40.7148, lng: -74.004 },
      { lat: 40.7158, lng: -74.003 },
    ],
    "AgroBot-02": [
      { lat: 40.7589, lng: -73.9851 },
      { lat: 40.7599, lng: -73.9841 },
      { lat: 40.7609, lng: -73.9831 },
      { lat: 40.7619, lng: -73.9821 },
    ],
    "AgroBot-03": [
      { lat: 40.7505, lng: -73.9934 },
      { lat: 40.7515, lng: -73.9924 },
      { lat: 40.7525, lng: -73.9914 },
    ],
  }

  useEffect(() => {
    if (!mapRef.current || !canvasRef.current) return

    const canvas = canvasRef.current
    const container = mapRef.current

    canvas.width = container.offsetWidth
    canvas.height = container.offsetHeight
    canvas.style.width = "100%"
    canvas.style.height = "100%"

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Draw background
    ctx.fillStyle = "#f8f9fa"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // Draw grid
    ctx.strokeStyle = "#e9ecef"
    ctx.lineWidth = 1
    for (let i = 0; i < canvas.width; i += 50) {
      ctx.beginPath()
      ctx.moveTo(i, 0)
      ctx.lineTo(i, canvas.height)
      ctx.stroke()
    }
    for (let i = 0; i < canvas.height; i += 50) {
      ctx.beginPath()
      ctx.moveTo(0, i)
      ctx.lineTo(canvas.width, i)
      ctx.stroke()
    }

    // Coordinate conversion functions
    const latToY = (lat: number) => {
      const normalizedLat = (lat - center.lat) * 10000
      return canvas.height / 2 - normalizedLat
    }

    const lngToX = (lng: number) => {
      const normalizedLng = (lng - center.lng) * 10000
      return canvas.width / 2 + normalizedLng
    }

    // Draw mission paths
    Object.entries(missionPaths).forEach(([robotId, path]) => {
      const robot = robots.find((r) => r.id === robotId)
      if (!robot || robot.status === "offline") return

      ctx.strokeStyle = robot.status === "active" ? "#22c55e" : "#94a3b8"
      ctx.lineWidth = 2
      ctx.setLineDash([5, 5])

      ctx.beginPath()
      path.forEach((point, index) => {
        const x = lngToX(point.lng)
        const y = latToY(point.lat)

        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }

        // Draw waypoint markers
        ctx.save()
        ctx.setLineDash([])
        ctx.fillStyle = "#ffffff"
        ctx.strokeStyle = "#6b7280"
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(x, y, 4, 0, 2 * Math.PI)
        ctx.fill()
        ctx.stroke()
        ctx.restore()
      })
      ctx.stroke()
      ctx.setLineDash([])
    })

    // Draw field boundaries (example)
    ctx.strokeStyle = "#059669"
    ctx.lineWidth = 3
    ctx.setLineDash([10, 5])
    ctx.strokeRect(50, 50, canvas.width - 100, canvas.height - 100)
    ctx.setLineDash([])

    // Draw robots
    robots.forEach((robot) => {
      const x = lngToX(robot.position.lng)
      const y = latToY(robot.position.lat)

      // Robot shadow
      ctx.fillStyle = "rgba(0, 0, 0, 0.2)"
      ctx.beginPath()
      ctx.arc(x + 2, y + 2, selectedRobot === robot.id ? 14 : 10, 0, 2 * Math.PI)
      ctx.fill()

      // Robot circle
      ctx.beginPath()
      ctx.arc(x, y, selectedRobot === robot.id ? 12 : 8, 0, 2 * Math.PI)

      // Status-based colors
      switch (robot.status) {
        case "active":
          ctx.fillStyle = "#22c55e"
          break
        case "idle":
          ctx.fillStyle = "#eab308"
          break
        case "warning":
          ctx.fillStyle = "#f97316"
          break
        case "offline":
          ctx.fillStyle = "#ef4444"
          break
        default:
          ctx.fillStyle = "#6b7280"
      }

      ctx.fill()

      // White border for selected robot
      if (selectedRobot === robot.id) {
        ctx.strokeStyle = "#ffffff"
        ctx.lineWidth = 3
        ctx.stroke()
      }

      // Robot icon (simplified)
      ctx.fillStyle = "#ffffff"
      ctx.font = "bold 8px sans-serif"
      ctx.textAlign = "center"
      ctx.fillText("🤖", x, y + 3)

      // Robot ID label
      ctx.fillStyle = "#000000"
      ctx.font = "10px sans-serif"
      ctx.textAlign = "center"
      ctx.fillText(robot.id.split("-")[1], x, y - 18)

      // Direction indicator
      if (robot.speed > 0) {
        const headingRad = (robot.heading * Math.PI) / 180
        const arrowLength = 15
        const arrowX = x + Math.sin(headingRad) * arrowLength
        const arrowY = y - Math.cos(headingRad) * arrowLength

        ctx.strokeStyle = "#000000"
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.moveTo(x, y)
        ctx.lineTo(arrowX, arrowY)
        ctx.stroke()

        // Arrow head
        const headSize = 4
        ctx.beginPath()
        ctx.moveTo(arrowX, arrowY)
        ctx.lineTo(
          arrowX - headSize * Math.sin(headingRad - Math.PI / 6),
          arrowY + headSize * Math.cos(headingRad - Math.PI / 6),
        )
        ctx.moveTo(arrowX, arrowY)
        ctx.lineTo(
          arrowX - headSize * Math.sin(headingRad + Math.PI / 6),
          arrowY + headSize * Math.cos(headingRad + Math.PI / 6),
        )
        ctx.stroke()
      }

      // Battery indicator
      if (robot.battery < 30) {
        ctx.fillStyle = robot.battery < 15 ? "#ef4444" : "#f97316"
        ctx.font = "12px sans-serif"
        ctx.fillText("⚠", x + 15, y - 10)
      }
    })

    // Handle clicks
    const handleClick = (event: MouseEvent) => {
      const rect = canvas.getBoundingClientRect()
      const clickX = event.clientX - rect.left
      const clickY = event.clientY - rect.top

      let clickedRobot: Robot | null = null

      // Check if click is near any robot
      robots.forEach((robot) => {
        const robotX = lngToX(robot.position.lng)
        const robotY = latToY(robot.position.lat)
        const distance = Math.sqrt((clickX - robotX) ** 2 + (clickY - robotY) ** 2)

        if (distance < 15) {
          clickedRobot = robot
          onRobotSelect(robot.id)
        }
      })

      if (clickedRobot) {
        setPopup({
          robot: clickedRobot,
          x: event.clientX - rect.left,
          y: event.clientY - rect.top,
          visible: true,
        })
      } else {
        setPopup((prev) => ({ ...prev, visible: false }))
      }
    }

    canvas.addEventListener("click", handleClick)

    return () => {
      canvas.removeEventListener("click", handleClick)
    }
  }, [robots, center, selectedRobot, onRobotSelect])

  const handleViewFleet = (robotId: string) => {
    router.push(`/fleet?robot=${robotId}`)
    setPopup((prev) => ({ ...prev, visible: false }))
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

  return (
    <div className="relative w-full h-full">
      <div ref={mapRef} className="w-full h-full bg-gray-50 border rounded-lg overflow-hidden">
        <canvas ref={canvasRef} className="w-full h-full cursor-pointer" />
      </div>

      {/* Robot Popup */}
      {popup.visible && popup.robot && (
        <div
          className="absolute z-50 pointer-events-auto"
          style={{
            left: Math.min(popup.x, (mapRef.current?.offsetWidth || 0) - 280),
            top: Math.max(popup.y - 200, 10),
          }}
        >
          <Card className="w-64 shadow-lg border-2">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm font-medium">{popup.robot.id}</CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0"
                  onClick={() => setPopup((prev) => ({ ...prev, visible: false }))}
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${getStatusColor(popup.robot.status)}`} />
                <Badge variant="outline" className="text-xs">
                  {popup.robot.status.toUpperCase()}
                </Badge>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="flex items-center gap-1">
                  <Battery className="h-3 w-3" />
                  <span>{popup.robot.battery}%</span>
                </div>
                <div className="flex items-center gap-1">
                  <Navigation className="h-3 w-3" />
                  <span>{popup.robot.speed} m/s</span>
                </div>
              </div>

              <div className="text-xs text-muted-foreground">
                <div className="flex items-center gap-1 mb-1">
                  <MapPin className="h-3 w-3" />
                  <span>Mission: {popup.robot.mission}</span>
                </div>
                <div>
                  Position: {popup.robot.position.lat.toFixed(4)}, {popup.robot.position.lng.toFixed(4)}
                </div>
              </div>

              <Button size="sm" className="w-full" onClick={() => handleViewFleet(popup.robot!.id)}>
                <ExternalLink className="h-3 w-3 mr-1" />
                View in Fleet
              </Button>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Map Legend */}
      <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-3 shadow-lg">
        <div className="text-xs font-medium mb-2">Legend</div>
        <div className="space-y-1 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span>Active</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <span>Idle</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-orange-500" />
            <span>Warning</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <span>Offline</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-1 bg-green-500" style={{ clipPath: "polygon(0 0, 100% 0, 100% 50%, 0 50%)" }} />
            <span>Mission Path</span>
          </div>
        </div>
      </div>
    </div>
  )
}
