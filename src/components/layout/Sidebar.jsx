import { NavLink } from 'react-router-dom'
import { dashboardRoutes } from '../../data/routes'

export function Sidebar() {
  return (
    <aside style={{ background: 'var(--bg-elev)', borderRight: '1px solid var(--border)', padding: 16 }}>
      <h2 style={{ marginTop: 0 }}>Cooler Master BR</h2>
      <p style={{ color: 'var(--muted)', marginTop: -8, marginBottom: 16 }}>React Dashboard Suite</p>
      <nav style={{ display: 'grid', gap: 8 }}>
        {dashboardRoutes.map((route) => (
          <NavLink
            key={route.path}
            to={route.path}
            style={({ isActive }) => ({
              padding: '10px 12px',
              borderRadius: 10,
              background: isActive ? 'var(--primary-soft)' : 'transparent',
              border: `1px solid ${isActive ? '#3d64d8' : 'var(--border)'}`,
              color: isActive ? '#fff' : 'var(--text)',
            })}
          >
            {route.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
