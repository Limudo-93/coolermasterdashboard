import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function PlaybookPage() {
  return <DashboardPage data={dashboards.playbook} />
}
