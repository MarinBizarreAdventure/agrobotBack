"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import dynamic from "next/dynamic"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ExternalLink, Battery, Navigation, MapPin } from "lucide-react"
import type { Robot } from "@/lib/types"
import { createRobotIcon, createMissionPath } from "@/lib/utils/map"
import { moldovaMissionPaths, moldovaFields } from "@/lib/mock/moldova-data"

// Dynamically import Leaflet to avoid SSR issues
const MapContainer = dynamic(() => import("react-leaflet").then((mod) => mod.MapContainer), { ssr: false })
const TileLayer = dynamic(() => import("react-leaflet").then((mod) => mod.TileLayer), { ssr: false })
const Marker = dynamic(() => import("react-leaflet").then((mod) => mod.Marker), { ssr: false })
const Popup = dynamic(() => import("react-leaflet").then((mod) => mod.Popup), { ssr: false })
const Polyline = dynamic(() => import("react-leaflet").then((mod) => mod.Polyline), { ssr: false })
const Polygon = dynamic(() => import("react-leaflet").then((mod) => mod.Polygon), { ssr: false })
const CircleMarker = dynamic(() => import("react-leaflet").then((mod) => mod.CircleMarker), { ssr: false })

interface LeafletMapProps {
  robots: Robot[]
  center: { lat: number; lng: number }
  zoom?: number
  selectedRobot: string | null
  onRobotSelect: (robotId: string) => void
  showMissions?: boolean
  showFields?: boolean
  className?: string
}

export function LeafletMap({
  robots,
  center,
  zoom = 12,
  selectedRobot,
  onRobotSelect,
  showMissions = true,
  showFields = true,
  className = "",
}: LeafletMapProps) {
  const [leafletLoaded, setLeafletLoaded] = useState(false)
  const router = useRouter()

  useEffect(() => {
    // Load Leaflet CSS
    if (typeof window !== "undefined") {
      const link = document.createElement("link")
      link.rel = "stylesheet"
      link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
      document.head.appendChild(link)

      // Load Leaflet JS
      const script = document.createElement("script")
      script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
      script.onload = () => setLeafletLoaded(true)
      document.head.appendChild(script)

      return () => {
        document.head.removeChild(link)
        document.head.removeChild(script)
      }
    }
  }, [])

  const handleRobotClick = (robot: Robot) => {
    onRobotSelect(robot.id)
  }

  const handleViewFleet = (robotId: string) => {
    router.push(`/fleet/${robotId}`)
  }

  if (!leafletLoaded) {
    return (
      <div className={`w-full h-full bg-gray-100 rounded-lg flex items-center justify-center ${className}`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
          <p className="text-sm text-muted-foreground">Loading map...</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`relative w-full h-full ${className}`}>
      <MapContainer
        center={[center.lat, center.lng]}
        zoom={zoom}
        style={{ height: "100%", width: "100%" }}
        className="rounded-lg"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Moldova Field Boundaries */}
        {showFields &&
          moldovaFields.map((field) => (
            <Polygon
              key={field.id}
              positions={field.boundaries.map((pos) => [pos.lat, pos.lng])}
              pathOptions={{
                color: "#059669",
                weight: 3,
                opacity: 0.8,
                fillOpacity: 0.1,
                fillColor: "#059669",
              }}
            >
              <Popup>
                <div className="text-sm">
                  <strong>{field.name}</strong>
                  <br />
                  Crop: {field.cropType}
                  <br />
                  Area: {field.area} ha
                  <br />
                  Coverage: {field.coverage}%
                </div>
              </Popup>
            </Polygon>
          ))}

        {/* Mission Paths in Moldova */}
        {showMissions &&
          Object.entries(moldovaMissionPaths).map(([robotId, path]) => {
            const robot = robots.find((r) => r.id === robotId)
            if (!robot) return null

            const pathStyle = createMissionPath(robot.status === "active" ? "active" : "planned")

            return (
              <Polyline
                key={`mission-${robotId}`}
                positions={path.map((pos) => [pos.lat, pos.lng])}
                pathOptions={pathStyle}
              >
                <Popup>
                  <div className="text-sm">
                    <strong>{robot.id}</strong>
                    <br />
                    Mission: {robot.mission}
                  </div>
                </Popup>
              </Polyline>
            )
          })}

        {/* Waypoints */}
        {showMissions &&
          Object.entries(moldovaMissionPaths).map(([robotId, path]) =>
            path.map((waypoint, index) => (
              <CircleMarker
                key={`waypoint-${robotId}-${index}`}
                center={[waypoint.lat, waypoint.lng]}
                pathOptions={{
                  color: "#3b82f6",
                  fillColor: "#ffffff",
                  radius: 4,
                  weight: 2,
                  fillOpacity: 0.8,
                }}
              >
                <Popup>
                  <div className="text-sm">
                    <strong>Waypoint {index + 1}</strong>
                    <br />
                    Robot: {robotId}
                  </div>
                </Popup>
              </CircleMarker>
            )),
          )}

        {/* Robots */}
        {robots.map((robot) => (
          <CircleMarker
            key={robot.id}
            center={[robot.position.lat, robot.position.lng]}
            pathOptions={createRobotIcon(robot.status, selectedRobot === robot.id)}
            eventHandlers={{
              click: () => handleRobotClick(robot),
            }}
          >
            <Popup>
              <div className="min-w-[200px]">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium">{robot.id}</h3>
                  <Badge variant="outline" className="text-xs">
                    {robot.status.toUpperCase()}
                  </Badge>
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <Battery className="h-3 w-3" />
                    <span>{robot.battery}%</span>
                    <Navigation className="h-3 w-3 ml-2" />
                    <span>{robot.speed} m/s</span>
                  </div>

                  <div className="flex items-center gap-1">
                    <MapPin className="h-3 w-3" />
                    <span className="text-xs">{robot.mission}</span>
                  </div>

                  <div className="text-xs text-muted-foreground">
                    {robot.position.lat.toFixed(4)}, {robot.position.lng.toFixed(4)}
                  </div>

                  <Button size="sm" className="w-full mt-2" onClick={() => handleViewFleet(robot.id)}>
                    <ExternalLink className="h-3 w-3 mr-1" />
                    View Robot Details
                  </Button>
                </div>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>

      {/* Map Legend */}
      <div className="absolute bottom-4 left-4 bg-white/95 backdrop-blur-sm rounded-lg p-3 shadow-lg border">
        <div className="text-xs font-medium mb-2">Moldova Agricultural Map</div>
        <div className="space-y-1 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span>Active Robot</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <span>Idle Robot</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-orange-500" />
            <span>Warning</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-0.5 bg-blue-500 border-dashed border-blue-500" />
            <span>Mission Path</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-0.5 bg-green-600" />
            <span>Agricultural Field</span>
          </div>
        </div>
      </div>
    </div>
  )
}
