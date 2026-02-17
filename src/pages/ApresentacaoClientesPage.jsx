import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function ApresentacaoClientesPage() {
  return <DashboardPage data={dashboards.clientes} />
}
