"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

const data = [
  { day: "Mon", completed: 8, planned: 10 },
  { day: "Tue", completed: 12, planned: 14 },
  { day: "Wed", completed: 15, planned: 16 },
  { day: "Thu", completed: 11, planned: 12 },
  { day: "Fri", completed: 14, planned: 15 },
  { day: "Sat", completed: 9, planned: 10 },
  { day: "Sun", completed: 7, planned: 8 },
]

export function MissionProgressChart() {
  return (
    <div className="h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="completed" stroke="#22c55e" strokeWidth={2} name="Completed" />
          <Line
            type="monotone"
            dataKey="planned"
            stroke="#3b82f6"
            strokeWidth={2}
            strokeDasharray="5 5"
            name="Planned"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
