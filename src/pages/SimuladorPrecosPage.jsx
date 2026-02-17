import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function SimuladorPrecosPage() {
  return <DashboardPage data={dashboards.simulador} />
}
