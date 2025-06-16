import { DashboardLayout } from "@/components/dashboard-layout"
import { RobotDetails } from "@/components/robot-details"

interface RobotPageProps {
  params: {
    robotId: string
  }
}

export default function RobotPage({ params }: RobotPageProps) {
  return (
    <DashboardLayout>
      <RobotDetails robotId={params.robotId} />
    </DashboardLayout>
  )
}
