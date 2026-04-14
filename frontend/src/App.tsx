import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from 'antd'
import AppHeader from './components/Layout/Header'
import Sidebar from './components/Layout/Sidebar'

import Dashboard from './pages/Dashboard'
import DataSources from './pages/DataSources'
import Rules from './pages/Rules'
import RuleDetail from './pages/RuleDetail'
import Executions from './pages/Executions'
import Alerts from './pages/Alerts'
import Login from './pages/Login'

const { Content } = Layout

function App() {
  return (
    <BrowserRouter>
      <Layout style={{ minHeight: '100vh' }}>
        <AppHeader />
        <Layout>
          <Sidebar />
          <Layout style={{ padding: '24px' }}>
            <Content style={{ background: '#f0f2f5', borderRadius: 8 }}>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/datasources" element={<DataSources />} />
                <Route path="/rules" element={<Rules />} />
                <Route path="/rules/:id" element={<RuleDetail />} />
                <Route path="/executions" element={<Executions />} />
                <Route path="/alerts" element={<Alerts />} />
              </Routes>
            </Content>
          </Layout>
        </Layout>
      </Layout>
    </BrowserRouter>
  )
}

export default App
