import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function CatalogoPage() {
  return <DashboardPage data={dashboards.catalogo} />
}
