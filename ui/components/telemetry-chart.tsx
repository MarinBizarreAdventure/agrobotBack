"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

interface TelemetryChartProps {
  robotId: string;
}

// Mock telemetry data
const generateTelemetryData = (robotId: string) => {
  const data = [];
  const now = Date.now();

  // Determine if the system should be shown as degraded based on robotId
  const isSystemDegraded = robotId === "agrobot-01";

  for (let i = 29; i >= 0; i--) {
    data.push({
      time: new Date(now - i * 60000).toLocaleTimeString("en-US", {
        hour12: false,
        hour: "2-digit",
        minute: "2-digit",
      }),
      battery: isSystemDegraded
        ? Math.max(0, 5 - Math.random() * 5)
        : Math.max(20, 100 - Math.random() * 30 - i * 0.5), // Show very low or 0 battery
      cpu: isSystemDegraded ? Math.random() * 10 : 20 + Math.random() * 60, // Show very low CPU
      memory: isSystemDegraded ? Math.random() * 10 : 30 + Math.random() * 50, // Show very low Memory
      temperature: isSystemDegraded
        ? Math.random() * 5
        : 35 + Math.random() * 20, // Show very low Temp
    });
  }

  return data;
};

export function TelemetryChart({ robotId }: TelemetryChartProps) {
  const data = generateTelemetryData(robotId);

  return (
    <div className="h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="time"
            tick={{ fontSize: 12 }}
            interval="preserveStartEnd"
          />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="battery"
            stroke="#22c55e"
            strokeWidth={2}
            name="Battery (%)"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="cpu"
            stroke="#3b82f6"
            strokeWidth={2}
            name="CPU (%)"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="memory"
            stroke="#f59e0b"
            strokeWidth={2}
            name="Memory (%)"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="temperature"
            stroke="#ef4444"
            strokeWidth={2}
            name="Temp (°C)"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
