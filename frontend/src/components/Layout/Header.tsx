import { Layout, Typography, Space } from 'antd'
import { DatabaseOutlined, BellOutlined, UserOutlined } from '@ant-design/icons'

const { Header } = Layout
const { Text } = Typography

const AppHeader = () => {
  return (
    <Header style={{
      background: '#001529',
      padding: '0 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      <Space>
        <DatabaseOutlined style={{ fontSize: 24, color: '#1890ff' }} />
        <Text strong style={{ color: '#fff', fontSize: 18 }}>
          DataQGuard
        </Text>
      </Space>

      <Space size="large">
        <BellOutlined style={{ fontSize: 18, color: '#fff', cursor: 'pointer' }} />
        <UserOutlined style={{ fontSize: 18, color: '#fff', cursor: 'pointer' }} />
      </Space>
    </Header>
  )
}

export default AppHeader
