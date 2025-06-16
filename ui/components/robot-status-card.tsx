"use client"

import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { Battery, MapPin, Play, Pause, MoreHorizontal } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

interface Robot {
  id: string
  status: "active" | "idle" | "warning" | "offline"
  mission: string
  battery: number
  position?: { lat: number; lng: number }
  progress: number
}

interface RobotStatusCardProps {
  robot: Robot
}

export function RobotStatusCard({ robot }: RobotStatusCardProps) {
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

  return (
    <div className="flex items-center justify-between p-4 border rounded-lg">
      <div className="flex items-center space-x-4">
        <div className="relative">
          <div className={`w-3 h-3 rounded-full ${getStatusColor(robot.status)}`} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium">{robot.id}</p>
            {getStatusBadge(robot.status)}
          </div>
          <p className="text-sm text-muted-foreground truncate">{robot.mission}</p>
          <div className="flex items-center space-x-4 mt-2">
            <div className="flex items-center space-x-1">
              <Battery className="h-3 w-3" />
              <span className="text-xs">{robot.battery}%</span>
            </div>
            <div className="flex items-center space-x-1">
              <MapPin className="h-3 w-3" />
              <span className="text-xs">
                {robot.position ? `${robot.position.lat.toFixed(4)}, ${robot.position.lng.toFixed(4)}` : "No GPS"}
              </span>
            </div>
          </div>
          <div className="mt-2">
            <div className="flex items-center justify-between text-xs mb-1">
              <span>Mission Progress</span>
              <span>{robot.progress}%</span>
            </div>
            <Progress value={robot.progress} className="h-1" />
          </div>
        </div>
      </div>
      <div className="flex items-center space-x-2">
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
            <DropdownMenuItem>View Details</DropdownMenuItem>
            <DropdownMenuItem>Send to Location</DropdownMenuItem>
            <DropdownMenuItem>Return Home</DropdownMenuItem>
            <DropdownMenuItem className="text-red-600">Emergency Stop</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  )
}
