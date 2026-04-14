import { Card, Descriptions, Button, Space, Tag, Timeline, Typography, Progress } from 'antd'
import { useParams } from 'react-router-dom'
import { PlayCircleOutlined, EditOutlined } from '@ant-design/icons'

const { Title } = Typography

const RuleDetail = () => {
  const { id } = useParams()

  // Mock data - replace with API call
  const rule = {
    id,
    name: 'Orders Completeness Check',
    description: 'Ensure critical fields in orders table are never null',
    datasource: { id: 1, name: 'Production DB' },
    table_name: 'orders',
    rule_type: 'completeness',
    schedule: '0 */4 * * *',
    is_active: true,
    created_at: '2026-01-15',
    last_run: '2026-04-14 10:00:00',
    last_result: { status: 'success', pass_rate: 98.5, total_rows: 15420, failed_rows: 231 }
  }

  const columns = [
    { column: 'order_id', completeness: 100 },
    { column: 'customer_id', completeness: 99.8 },
    { column: 'amount', completeness: 100 },
    { column: 'created_at', completeness: 98.5 },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 24 }}>
        <Title level={3}>{rule.name}</Title>
        <Space>
          <Button icon={<PlayCircleOutlined />}>Run Now</Button>
          <Button icon={<EditOutlined />}>Edit</Button>
        </Space>
      </div>

      <Card title="Rule Details" style={{ marginBottom: 16 }}>
        <Descriptions column={2}>
          <Descriptions.Item label="Name">{rule.name}</Descriptions.Item>
          <Descriptions.Item label="Status">
            {rule.is_active ? <Tag color="green">Active</Tag> : <Tag>Paused</Tag>}
          </Descriptions.Item>
          <Descriptions.Item label="Data Source">{rule.datasource.name}</Descriptions.Item>
          <Descriptions.Item label="Table">{rule.table_name}</Descriptions.Item>
          <Descriptions.Item label="Rule Type">
            <Tag color="blue">{rule.rule_type}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="Schedule">
            <code>{rule.schedule}</code>
          </Descriptions.Item>
          <Descriptions.Item label="Created">{rule.created_at}</Descriptions.Item>
          <Descriptions.Item label="Last Run">{rule.last_run}</Descriptions.Item>
          <Descriptions.Item label="Description" span={2}>{rule.description}</Descriptions.Item>
        </Descriptions>
      </Card>

      <Card title="Column Completeness" style={{ marginBottom: 16 }}>
        {columns.map(col => (
          <div key={col.column} style={{ marginBottom: 12 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
              <span><code>{col.column}</code></span>
              <span style={{ color: col.completeness < 99 ? '#ff4d4f' : '#52c41a' }}>
                {col.completeness}%
              </span>
            </div>
            <Progress
              percent={col.completeness}
              status={col.completeness < 99 ? 'exception' : 'success'}
              showInfo={false}
            />
          </div>
        ))}
      </Card>

      <Card title="Execution History">
        <Timeline
          items={[
            { color: 'green', children: 'Success - 2026-04-14 10:00 - Pass Rate: 98.5%' },
            { color: 'green', children: 'Success - 2026-04-14 06:00 - Pass Rate: 99.2%' },
            { color: 'green', children: 'Success - 2026-04-14 02:00 - Pass Rate: 100%' },
            { color: 'red', children: 'Failed - 2026-04-13 22:00 - Connection timeout' },
          ]}
        />
      </Card>
    </div>
  )
}

export default RuleDetail
