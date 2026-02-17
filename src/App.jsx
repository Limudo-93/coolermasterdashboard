import { useEffect, useMemo, useState } from 'react'
import './App.css'

const DASHBOARDS = [
  { key: 'hub', label: 'Hub', file: 'CM_Brasil_Hub.html', section: 'Navegação' },
  { key: 'masterdeck', label: 'MasterDeck', file: 'CM_Brasil_MasterDeck.html', section: 'Executivo' },
  { key: 'forecast', label: 'Forecast', file: 'CM_Forecast_Dashboard.html', section: 'Operacional' },
  { key: 'catalogo', label: 'Catálogo', file: 'CM_Catalogo_Dashboard.html', section: 'Operacional' },
  { key: 'sellout', label: 'Sell-Out Tracker', file: 'CM_SellOut_Tracker.html', section: 'Operacional' },
  { key: 'simulador', label: 'Simulador de Preços', file: 'CM_Simulador_Precos.html', section: 'Operacional' },
  { key: 'followup', label: 'Follow-Up Tracker', file: 'CM_FollowUp_Tracker.html', section: 'Operacional' },
  { key: 'playbook', label: 'Playbook', file: 'CM_Playbook_Processos.html', section: 'Referência' },
  { key: 'platform', label: 'Jubinha Platform', file: 'CM_Jubinha_Platform.html', section: 'Referência' },
  { key: 'ap-int', label: 'Apresentação Interna', file: 'CM_Apresentacao_Interna.html', section: 'Apresentações' },
  { key: 'ap-cli', label: 'Apresentação Clientes', file: 'CM_Apresentacao_Clientes.html', section: 'Apresentações' },
]

function App() {
  const initial = window.location.hash?.replace('#', '') || 'hub'
  const [active, setActive] = useState(initial)

  useEffect(() => {
    const next = window.location.hash?.replace('#', '')
    if (next && DASHBOARDS.some((d) => d.key === next)) setActive(next)
    const onHash = () => {
      const h = window.location.hash?.replace('#', '')
      if (h && DASHBOARDS.some((d) => d.key === h)) setActive(h)
    }
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  const current = useMemo(
    () => DASHBOARDS.find((d) => d.key === active) ?? DASHBOARDS[0],
    [active],
  )

  const grouped = useMemo(() => {
    return DASHBOARDS.reduce((acc, d) => {
      if (!acc[d.section]) acc[d.section] = []
      acc[d.section].push(d)
      return acc
    }, {})
  }, [])

  const openDashboard = (key) => {
    setActive(key)
    window.location.hash = key
  }

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          <h1>CM Brasil</h1>
          <p>Dashboards Unificados</p>
        </div>

        {Object.entries(grouped).map(([section, items]) => (
          <div className="menu-group" key={section}>
            <div className="menu-title">{section}</div>
            {items.map((d) => (
              <button
                key={d.key}
                className={`menu-item ${active === d.key ? 'active' : ''}`}
                onClick={() => openDashboard(d.key)}
              >
                {d.label}
              </button>
            ))}
          </div>
        ))}
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h2>{current.label}</h2>
            <span>/dashboards/{current.file}</span>
          </div>
          <a href={`/dashboards/${current.file}`} target="_blank" rel="noreferrer">
            Abrir em nova aba
          </a>
        </header>

        <div className="viewer">
          <iframe
            key={current.file}
            src={`/dashboards/${current.file}`}
            title={current.label}
            loading="lazy"
            referrerPolicy="no-referrer"
          />
        </div>
      </main>
    </div>
  )
}

export default App
