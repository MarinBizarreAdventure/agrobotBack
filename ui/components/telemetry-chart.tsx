"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

// Mock telemetry data
const generateTelemetryData = () => {
  const data = []
  const now = Date.now()

  for (let i = 29; i >= 0; i--) {
    data.push({
      time: new Date(now - i * 60000).toLocaleTimeString("en-US", {
        hour12: false,
        hour: "2-digit",
        minute: "2-digit",
      }),
      battery: Math.max(20, 100 - Math.random() * 30 - i * 0.5),
      cpu: 20 + Math.random() * 60,
      memory: 30 + Math.random() * 50,
      temperature: 35 + Math.random() * 20,
    })
  }

  return data
}

interface TelemetryChartProps {
  robotId: string
}

export function TelemetryChart({ robotId }: TelemetryChartProps) {
  const data = generateTelemetryData()

  return (
    <div className="h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" tick={{ fontSize: 12 }} interval="preserveStartEnd" />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="battery" stroke="#22c55e" strokeWidth={2} name="Battery (%)" dot={false} />
          <Line type="monotone" dataKey="cpu" stroke="#3b82f6" strokeWidth={2} name="CPU (%)" dot={false} />
          <Line type="monotone" dataKey="memory" stroke="#f59e0b" strokeWidth={2} name="Memory (%)" dot={false} />
          <Line type="monotone" dataKey="temperature" stroke="#ef4444" strokeWidth={2} name="Temp (°C)" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
