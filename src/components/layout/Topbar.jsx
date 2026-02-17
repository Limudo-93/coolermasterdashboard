export function Topbar({ title, subtitle }) {
  return (
    <header style={{ marginBottom: 16 }}>
      <h1 style={{ margin: 0, fontSize: 30 }}>{title}</h1>
      <p style={{ margin: '6px 0 0', color: 'var(--muted)' }}>{subtitle}</p>
    </header>
  )
}
