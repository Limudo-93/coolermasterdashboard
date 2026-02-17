import { Topbar } from '../components/layout/Topbar'
import { SectionCard } from '../components/layout/SectionCard'
import { KPICard } from '../components/layout/KPICard'
import { DataTable } from '../components/layout/DataTable'
import { MixBarChart, RevenueLineChart } from '../components/charts/SimpleCharts'

export function DashboardPage({ data }) {
  return (
    <div className="page-grid">
      <Topbar title={data.title} subtitle={data.subtitle} />

      <div className="kpi-grid">
        {data.kpis.map((kpi) => (
          <KPICard key={kpi.label} {...kpi} />
        ))}
      </div>

      <div className="chart-grid">
        <SectionCard title="Tendência principal">
          <RevenueLineChart labels={data.chartLabels} data={data.chartValues} />
        </SectionCard>
        <SectionCard title="Distribuição / Mix">
          <MixBarChart labels={data.chartLabels.slice(0, data.mixValues.length)} data={data.mixValues} />
        </SectionCard>
      </div>

      <SectionCard title="Tabela principal">
        <DataTable columns={data.tableColumns} rows={data.tableRows} />
      </SectionCard>
    </div>
  )
}
