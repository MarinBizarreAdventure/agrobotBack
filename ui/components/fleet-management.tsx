"use client"

import { useSearchParams } from "next/navigation"
import { useEffect, useState } from "react"

export function FleetManagement() {
  const searchParams = useSearchParams()
  const highlightRobotId = searchParams?.get("robot")
  const [robots, setRobots] = useState([
    { id: "robot-1", name: "Robot 1" },
    { id: "robot-2", name: "Robot 2" },
    { id: "robot-3", name: "Robot 3" },
  ])

  useEffect(() => {
    if (highlightRobotId) {
      // Scroll to and highlight the specific robot
      const robotElement = document.getElementById(`robot-${highlightRobotId}`)
      if (robotElement) {
        robotElement.scrollIntoView({ behavior: "smooth", block: "center" })
        robotElement.classList.add("ring-2", "ring-blue-500", "ring-offset-2")

        // Remove highlight after 3 seconds
        setTimeout(() => {
          robotElement.classList.remove("ring-2", "ring-blue-500", "ring-offset-2")
        }, 3000)
      }
    }
  }, [highlightRobotId])

  return (
    <div>
      <h1>Fleet Management</h1>
      <div className="flex flex-col gap-4">
        {robots.map((robot) => (
          <div id={`robot-${robot.id}`} key={robot.id} className="border p-4 rounded-md">
            <h2>{robot.name}</h2>
            <p>ID: {robot.id}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
