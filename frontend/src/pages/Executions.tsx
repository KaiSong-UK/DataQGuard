import { Table, Tag, Typography, Select, Space, Button } from 'antd'
import { RedoOutlined } from '@ant-design/icons'

const { Title } = Typography

interface Execution {
  id: number
  rule_id: number
  rule_name: string
  status: string
  started_at: string
  completed_at: string
  duration: string
  total_rows: number
  failed_rows: number
  pass_rate: number
}

const Executions = () => {
  const [executions] = useState<Execution[]>([
    { id: 10, rule_id: 1, rule_name: 'Orders Completeness', status: 'success', started_at: '2026-04-14 10:00', completed_at: '2026-04-14 10:02', duration: '2m', total_rows: 15420, failed_rows: 231, pass_rate: 98.5 },
    { id: 9, rule_id: 2, rule_name: 'Users Email Validity', status: 'success', started_at: '2026-04-14 09:00', completed_at: '2026-04-14 09:03', duration: '3m', total_rows: 45230, failed_rows: 0, pass_rate: 100 },
    { id: 8, rule_id: 3, rule_name: 'Products Unique SKU', status: 'failed', started_at: '2026-04-14 08:00', completed_at: '2026-04-14 08:01', duration: '1m', total_rows: 0, failed_rows: 0, pass_rate: 0 },
    { id: 7, rule_id: 1, rule_name: 'Orders Completeness', status: 'success', started_at: '2026-04-14 06:00', completed_at: '2026-04-14 06:02', duration: '2m', total_rows: 15200, failed_rows: 120, pass_rate: 99.2 },
  ])

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
    { title: 'Rule ID', dataIndex: 'rule_id', key: 'rule_id', width: 80 },
    { title: 'Rule Name', dataIndex: 'rule_name', key: 'rule_name' },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const colors: Record<string, string> = { success: 'green', failed: 'red', running: 'blue', pending: 'orange' }
        return <Tag color={colors[status]}>{status.toUpperCase()}</Tag>
      }
    },
    { title: 'Started', dataIndex: 'started_at', key: 'started_at' },
    { title: 'Duration', dataIndex: 'duration', key: 'duration' },
    { title: 'Total Rows', dataIndex: 'total_rows', key: 'total_rows', render: (n: number) => n.toLocaleString() },
    { title: 'Failed', dataIndex: 'failed_rows', key: 'failed_rows', render: (n: number) => n.toLocaleString() },
    { title: 'Pass Rate', dataIndex: 'pass_rate', key: 'pass_rate', render: (r: number) => `${r}%` }
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Title level={3} style={{ margin: 0 }}>Execution History</Title>
        <Space>
          <Select placeholder="Status" allowClear style={{ width: 120 }}>
            <Select.Option value="success">Success</Select.Option>
            <Select.Option value="failed">Failed</Select.Option>
            <Select.Option value="running">Running</Select.Option>
          </Select>
          <Button icon={<RedoOutlined />}>Refresh</Button>
        </Space>
      </div>
      <Table columns={columns} dataSource={executions} rowKey="id" />
    </div>
  )
}

export default Executions
