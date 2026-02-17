import { Navigate, Route, Routes } from 'react-router-dom'
import { Sidebar } from './components/layout/Sidebar'
import HubPage from './pages/HubPage'
import MasterdeckPage from './pages/MasterdeckPage'
import CatalogoPage from './pages/CatalogoPage'
import SelloutTrackerPage from './pages/SelloutTrackerPage'
import ForecastPage from './pages/ForecastPage'
import SimuladorPrecosPage from './pages/SimuladorPrecosPage'
import FollowupPage from './pages/FollowupPage'
import PlaybookPage from './pages/PlaybookPage'
import JubinhaPlatformPage from './pages/JubinhaPlatformPage'
import ApresentacaoInternaPage from './pages/ApresentacaoInternaPage'
import ApresentacaoClientesPage from './pages/ApresentacaoClientesPage'

function App() {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Navigate to="/hub" replace />} />
          <Route path="/hub" element={<HubPage />} />
          <Route path="/masterdeck" element={<MasterdeckPage />} />
          <Route path="/catalogo" element={<CatalogoPage />} />
          <Route path="/sellout-tracker" element={<SelloutTrackerPage />} />
          <Route path="/forecast" element={<ForecastPage />} />
          <Route path="/simulador-precos" element={<SimuladorPrecosPage />} />
          <Route path="/followup" element={<FollowupPage />} />
          <Route path="/playbook" element={<PlaybookPage />} />
          <Route path="/jubinha-platform" element={<JubinhaPlatformPage />} />
          <Route path="/apresentacao-interna" element={<ApresentacaoInternaPage />} />
          <Route path="/apresentacao-clientes" element={<ApresentacaoClientesPage />} />
          <Route path="*" element={<Navigate to="/hub" replace />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
