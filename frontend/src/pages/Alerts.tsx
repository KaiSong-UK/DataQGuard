import { Card, List, Tag, Space, Button, Typography, Badge } from 'antd'
import { CheckOutlined, MailOutlined, SlackOutlined, BellOutlined } from '@ant-design/icons'

const { Title } = Typography

interface Alert {
  id: number
  rule_name: string
  severity: string
  message: string
  channel: string
  created_at: string
  is_sent: boolean
}

const Alerts = () => {
  const [alerts] = useState<Alert[]>([
    { id: 3, rule_name: 'Orders Completeness', severity: 'warning', message: 'customer_id completeness dropped to 99.8% (threshold: 99.5%)', channel: 'email', created_at: '2026-04-14 10:02', is_sent: false },
    { id: 2, rule_name: 'Products Unique SKU', severity: 'error', message: 'Execution failed: connection timeout', channel: 'slack', created_at: '2026-04-14 08:01', is_sent: true },
    { id: 1, rule_name: 'Transactions Freshness', severity: 'critical', message: 'No new transactions in 48 hours (max delay: 24h)', channel: 'dingtalk', created_at: '2026-04-13 23:00', is_sent: true },
  ])

  const getSeverityColor = (severity: string) => {
    const colors: Record<string, string> = { info: 'blue', warning: 'orange', error: 'red', critical: 'magenta' }
    return colors[severity] || 'default'
  }

  const getChannelIcon = (channel: string) => {
    const icons: Record<string, React.ReactNode> = {
      email: <MailOutlined />,
      slack: <SlackOutlined />,
      dingtalk: <BellOutlined />
    }
    return icons[channel] || <BellOutlined />
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Title level={3} style={{ margin: 0 }}>Alerts</Title>
        <Space>
          <Badge count={alerts.filter(a => !a.is_sent).length} style={{ backgroundColor: '#ff4d4f' }}>
            <Button>Pending</Button>
          </Badge>
        </Space>
      </div>

      <List
        itemLayout="horizontal"
        dataSource={alerts}
        renderItem={(alert) => (
          <List.Item
            actions={[
              alert.is_sent
                ? <Tag key="sent" color="green">Sent</Tag>
                : <Button key="ack" type="primary" size="small" icon={<CheckOutlined />}>Send</Button>
            ]}
          >
            <List.Item.Meta
              avatar={<span style={{ fontSize: 24 }}>{getChannelIcon(alert.channel)}</span>}
              title={
                <Space>
                  <Tag color={getSeverityColor(alert.severity)}>{alert.severity.toUpperCase()}</Tag>
                  <span>{alert.rule_name}</span>
                </Space>
              }
              description={
                <Space direction="vertical" size={0}>
                  <span>{alert.message}</span>
                  <span style={{ color: '#999', fontSize: 12 }}>{alert.created_at}</span>
                </Space>
              }
            />
          </List.Item>
        )}
      />
    </div>
  )
}

export default Alerts
