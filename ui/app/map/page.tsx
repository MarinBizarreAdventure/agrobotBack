import { DashboardLayout } from "@/components/dashboard-layout"
import { LiveMapInterface } from "@/components/live-map-interface"

export default function MapPage() {
  return (
    <DashboardLayout>
      <LiveMapInterface />
    </DashboardLayout>
  )
}
