"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts"
import type { Robot } from "@/lib/types"

interface FleetStatusChartProps {
  robots: Robot[]
}

export function FleetStatusChart({ robots }: FleetStatusChartProps) {
  const statusCounts = robots.reduce(
    (acc, robot) => {
      acc[robot.status] = (acc[robot.status] || 0) + 1
      return acc
    },
    {} as Record<string, number>,
  )

  const data = [
    { name: "Active", value: statusCounts.active || 0, color: "#22c55e" },
    { name: "Idle", value: statusCounts.idle || 0, color: "#eab308" },
    { name: "Warning", value: statusCounts.warning || 0, color: "#f97316" },
    { name: "Offline", value: statusCounts.offline || 0, color: "#ef4444" },
    { name: "Maintenance", value: statusCounts.maintenance || 0, color: "#8b5cf6" },
  ].filter((item) => item.value > 0)

  return (
    <div className="h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={5} dataKey="value">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
