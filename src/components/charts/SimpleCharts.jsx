import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Bar, Line } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend)

const baseOptions = {
  responsive: true,
  plugins: { legend: { labels: { color: '#e7ecf7' } } },
  scales: {
    x: { ticks: { color: '#9aaccc' }, grid: { color: '#24314f' } },
    y: { ticks: { color: '#9aaccc' }, grid: { color: '#24314f' } },
  },
}

export function RevenueLineChart({ labels, data, label = 'Receita' }) {
  return <Line options={baseOptions} data={{ labels, datasets: [{ label, data, borderColor: '#3b82f6', backgroundColor: '#3b82f633' }] }} />
}

export function MixBarChart({ labels, data, label = 'Mix' }) {
  return <Bar options={baseOptions} data={{ labels, datasets: [{ label, data, backgroundColor: '#10b981aa' }] }} />
}
