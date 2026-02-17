import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function FollowupPage() {
  return <DashboardPage data={dashboards.followup} />
}
