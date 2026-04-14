import { useState } from 'react'
import { Layout, Menu } from 'antd'
import {
  DashboardOutlined,
  DatabaseOutlined,
  ProjectOutlined,
  PlayCircleOutlined,
  AlertOutlined
} from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'

const { Sider } = Layout

const menuItems = [
  { key: '/dashboard', icon: <DashboardOutlined />, label: 'Dashboard' },
  { key: '/datasources', icon: <DatabaseOutlined />, label: 'Data Sources' },
  { key: '/rules', icon: <ProjectOutlined />, label: 'Rules' },
  { key: '/executions', icon: <PlayCircleOutlined />, label: 'Executions' },
  { key: '/alerts', icon: <AlertOutlined />, label: 'Alerts' },
]

const Sidebar = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const [collapsed, setCollapsed] = useState(false)

  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key)
  }

  return (
    <Sider
      collapsible
      collapsed={collapsed}
      onCollapse={setCollapsed}
      style={{ background: '#fff' }}
    >
      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
        onClick={handleMenuClick}
        items={menuItems}
        style={{ height: '100%', borderRight: 0 }}
      />
    </Sider>
  )
}

export default Sidebar
