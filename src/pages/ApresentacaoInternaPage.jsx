import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function ApresentacaoInternaPage() {
  return <DashboardPage data={dashboards.interna} />
}
