import { useEffect, useMemo, useState } from 'react'
import './App.css'

const sections = [
  {
    title: 'Navegação',
    items: [{ id: 'hub', label: 'Hub', file: 'CM_Brasil_Hub.html' }],
  },
  {
    title: 'Executivo',
    items: [{ id: 'masterdeck', label: 'MasterDeck', file: 'CM_Brasil_MasterDeck.html' }],
  },
  {
    title: 'Operacional',
    items: [
      { id: 'catalogo', label: 'Catálogo', file: 'CM_Catalogo_Dashboard.html' },
      { id: 'sellout', label: 'Sell-Out', file: 'CM_SellOut_Tracker.html' },
      { id: 'forecast', label: 'Forecast', file: 'CM_Forecast_Dashboard.html' },
      { id: 'simulador', label: 'Simulador', file: 'CM_Simulador_Precos.html' },
      { id: 'followup', label: 'Follow-Up', file: 'CM_FollowUp_Tracker.html' },
    ],
  },
  {
    title: 'Referência',
    items: [
      { id: 'playbook', label: 'Playbook', file: 'CM_Playbook_Processos.html' },
      { id: 'jubinha', label: 'Jubinha Platform', file: 'CM_Jubinha_Platform.html' },
    ],
  },
  {
    title: 'Apresentações',
    items: [
      { id: 'interna', label: 'Interna', file: 'CM_Apresentacao_Interna.html' },
      { id: 'clientes', label: 'Clientes', file: 'CM_Apresentacao_Clientes.html' },
    ],
  },
]

const allItems = sections.flatMap((section) => section.items)

function resolveDashboardFromHash(hash) {
  const cleanHash = hash.replace(/^#/, '')
  return allItems.find((item) => item.id === cleanHash) || allItems[0]
}

export default function App() {
  const [active, setActive] = useState(() => resolveDashboardFromHash(window.location.hash))

  useEffect(() => {
    const onHashChange = () => {
      setActive(resolveDashboardFromHash(window.location.hash))
    }

    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const iframeSrc = useMemo(() => `/dashboards/${active.file}`, [active.file])

  const handleSelect = (item) => {
    window.location.hash = item.id
    setActive(item)
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">Cooler Master</div>

        {sections.map((section) => (
          <div className="section" key={section.title}>
            <div className="section-title">{section.title}</div>
            <div className="menu">
              {section.items.map((item) => (
                <button
                  key={item.id}
                  className={`menu-item ${active.id === item.id ? 'active' : ''}`}
                  onClick={() => handleSelect(item)}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </aside>

      <main className="content">
        <header className="topbar">
          <div className="title">{active.label}</div>
          <a className="new-tab" href={iframeSrc} target="_blank" rel="noreferrer">
            Abrir em nova aba
          </a>
        </header>

        <iframe
          key={active.id}
          src={iframeSrc}
          title={active.label}
          className="dashboard-frame"
          loading="eager"
        />
      </main>
    </div>
  )
}
