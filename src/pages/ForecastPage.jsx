import { DashboardPage } from './DashboardPage'
import { dashboards } from '../data/dashboardData'

export default function ForecastPage() {
  return <DashboardPage data={dashboards.forecast} />
}
