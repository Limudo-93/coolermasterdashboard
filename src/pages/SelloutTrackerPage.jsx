import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function SelloutTrackerPage() {
  return <DashboardPage data={dashboards.sellout} />
}
