import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function MasterdeckPage() {
  return <DashboardPage data={dashboards.masterdeck} />
}
