import { DashboardLayout } from "@/components/dashboard-layout"
import { FleetOverview } from "@/components/fleet-overview"

export default function FleetPage() {
  return (
    <DashboardLayout>
      <FleetOverview />
    </DashboardLayout>
  )
}
