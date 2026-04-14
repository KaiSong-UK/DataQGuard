import { useState } from 'react'
import { Table, Button, Tag, Space, Typography, Input, Select, Card } from 'antd'
import { PlusOutlined, PlayCircleOutlined, PauseCircleOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const { Title } = Typography
const { Search } = Input
const { Option } = Select

interface Rule {
  id: number
  name: string
  datasource_name: string
  table_name: string
  rule_type: string
  schedule: string
  is_active: boolean
  last_run: string
  pass_rate: number
}

const Rules = () => {
  const navigate = useNavigate()
  const [rules] = useState<Rule[]>([
    { id: 1, name: 'Orders Completeness', datasource_name: 'Production DB', table_name: 'orders', rule_type: 'completeness', schedule: '0 */4 * * *', is_active: true, last_run: '2026-04-14 10:00', pass_rate: 98.5 },
    { id: 2, name: 'Users Email Validity', datasource_name: 'User Database', table_name: 'users', rule_type: 'accuracy', schedule: '0 2 * * *', is_active: true, last_run: '2026-04-14 02:00', pass_rate: 100 },
    { id: 3, name: 'Products Unique SKU', datasource_name: 'Production DB', table_name: 'products', rule_type: 'uniqueness', schedule: '0 */6 * * *', is_active: true, last_run: '2026-04-14 06:00', pass_rate: 95.2 },
    { id: 4, name: 'Transactions Freshness', datasource_name: 'Analytics DB', table_name: 'transactions', rule_type: 'timeliness', schedule: '0 * * * *', is_active: false, last_run: '2026-04-13 23:00', pass_rate: 0 },
    { id: 5, name: 'Inventory Stock Check', datasource_name: 'Production DB', table_name: 'inventory', rule_type: 'accuracy', schedule: '0 8 * * *', is_active: true, last_run: '2026-04-14 08:00', pass_rate: 99.8 },
  ])

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: Rule) => (
        <a onClick={() => navigate(`/rules/${record.id}`)}>{name}</a>
      )
    },
    { title: 'Data Source', dataIndex: 'datasource_name', key: 'datasource_name' },
    { title: 'Table', dataIndex: 'table_name', key: 'table_name' },
    {
      title: 'Type',
      dataIndex: 'rule_type',
      key: 'rule_type',
      render: (type: string) => {
        const colors: Record<string, string> = {
          completeness: 'blue',
          accuracy: 'green',
          uniqueness: 'purple',
          timeliness: 'orange'
        }
        return <Tag color={colors[type]}>{type}</Tag>
      }
    },
    { title: 'Schedule', dataIndex: 'schedule', key: 'schedule', render: (s: string) => <code>{s}</code> },
    {
      title: 'Status',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (active: boolean) => active
        ? <Tag color="green">Active</Tag>
        : <Tag color="default">Paused</Tag>
    },
    {
      title: 'Pass Rate',
      dataIndex: 'pass_rate',
      key: 'pass_rate',
      render: (rate: number, record: Rule) => (
        record.is_active
          ? <span style={{ color: rate < 90 ? '#ff4d4f' : '#52c41a' }}>{rate}%</span>
          : '-'
      )
    },
    {
      title: 'Last Run',
      dataIndex: 'last_run',
      key: 'last_run'
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Rule) => (
        <Space>
          <Button
            type="primary"
            size="small"
            icon={<PlayCircleOutlined />}
            onClick={() => console.log('Execute rule', record.id)}
          >
            Run
          </Button>
        </Space>
      )
    }
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Title level={3} style={{ margin: 0 }}>Rules</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/rules/new')}>
          Create Rule
        </Button>
      </div>

      <Card style={{ marginBottom: 16 }}>
        <Space wrap>
          <Search placeholder="Search rules..." style={{ width: 200 }} />
          <Select placeholder="Rule Type" allowClear style={{ width: 150 }}>
            <Option value="completeness">Completeness</Option>
            <Option value="accuracy">Accuracy</Option>
            <Option value="uniqueness">Uniqueness</Option>
            <Option value="timeliness">Timeliness</Option>
          </Select>
          <Select placeholder="Status" allowClear style={{ width: 120 }}>
            <Option value="active">Active</Option>
            <Option value="paused">Paused</Option>
          </Select>
        </Space>
      </Card>

      <Table columns={columns} dataSource={rules} rowKey="id" />
    </div>
  )
}

export default Rules
