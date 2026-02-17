export function KPICard({ label, value, trend }) {
  const trendColor = trend?.startsWith('-') ? 'var(--danger)' : 'var(--success)'
  return (
    <article style={{ background: 'var(--bg-soft)', border: '1px solid var(--border)', borderRadius: 10, padding: 12 }}>
      <small style={{ color: 'var(--muted)' }}>{label}</small>
      <div style={{ fontSize: 24, fontWeight: 700, marginTop: 4 }}>{value}</div>
      {trend && <div style={{ color: trendColor, marginTop: 6, fontSize: 13 }}>{trend}</div>}
    </article>
  )
}
