import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function HubPage() {
  return <DashboardPage data={dashboards.hub} />
}
