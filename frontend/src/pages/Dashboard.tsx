import { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Progress, Table, Tag, Space, Typography } from 'antd'
import {
  ProjectOutlined,
  CheckCircleOutlined,
  PlayCircleOutlined,
  AlertOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined
} from '@ant-design/icons'
import ReactECharts from 'echarts-for-react'

const { Title } = Typography

interface StatsData {
  total_rules: number
  active_rules: number
  total_executions: number
  pending_alerts: number
}

interface Execution {
  id: number
  rule_id: number
  status: string
  started_at: string
  pass_rate: number
}

const Dashboard = () => {
  const [stats, setStats] = useState<StatsData>({
    total_rules: 0,
    active_rules: 0,
    total_executions: 0,
    pending_alerts: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulated data - replace with actual API call
    setTimeout(() => {
      setStats({
        total_rules: 12,
        active_rules: 10,
        total_executions: 156,
        pending_alerts: 3
      })
      setLoading(false)
    }, 500)
  }, [])

  const getHealthOption = () => ({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value',
      min: 80,
      max: 100
    },
    series: [{
      name: 'Health Score',
      type: 'line',
      smooth: true,
      data: [95, 94, 96, 93, 97, 95, 96],
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(24, 144, 255, 0.4)' },
            { offset: 1, color: 'rgba(24, 144, 255, 0.05)' }
          ]
        }
      },
      lineStyle: { color: '#1890ff', width: 3 },
      itemStyle: { color: '#1890ff' }
    }]
  })

  const getRuleTypeOption = () => ({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: 5, name: 'Completeness' },
        { value: 3, name: 'Accuracy' },
        { value: 2, name: 'Uniqueness' },
        { value: 2, name: 'Timeliness' }
      ]
    }]
  })

  const executionColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Rule ID', dataIndex: 'rule_id', key: 'rule_id' },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const colors: Record<string, string> = {
          success: 'green',
          failed: 'red',
          running: 'blue',
          pending: 'orange'
        }
        return <Tag color={colors[status] || 'default'}>{status.toUpperCase()}</Tag>
      }
    },
    {
      title: 'Pass Rate',
      dataIndex: 'pass_rate',
      key: 'pass_rate',
      render: (rate: number) => (
        <Progress percent={rate} size="small" status={rate < 90 ? 'exception' : 'success'} />
      )
    }
  ]

  const mockExecutions: Execution[] = [
    { id: 1, rule_id: 3, status: 'success', started_at: '2026-04-14 10:00', pass_rate: 98.5 },
    { id: 2, rule_id: 5, status: 'success', started_at: '2026-04-14 09:00', pass_rate: 100 },
    { id: 3, rule_id: 2, status: 'failed', started_at: '2026-04-14 08:00', pass_rate: 0 },
    { id: 4, rule_id: 1, status: 'success', started_at: '2026-04-14 07:00', pass_rate: 95.2 },
    { id: 5, rule_id: 4, status: 'success', started_at: '2026-04-14 06:00', pass_rate: 99.8 },
  ]

  return (
    <div style={{ padding: 0 }}>
      <Title level={3} style={{ marginBottom: 24 }}>Dashboard</Title>

      {/* Stats Cards */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Total Rules"
              value={stats.total_rules}
              prefix={<ProjectOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Active Rules"
              value={stats.active_rules}
              prefix={<CheckCircleOutlined />}
              suffix={<span style={{ fontSize: 14, color: '#52c41a' }}><ArrowUpOutlined /> 2</span>}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Total Executions"
              value={stats.total_executions}
              prefix={<PlayCircleOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card loading={loading}>
            <Statistic
              title="Pending Alerts"
              value={stats.pending_alerts}
              prefix={<AlertOutlined />}
              valueStyle={{ color: stats.pending_alerts > 0 ? '#faad14' : '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Charts */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={16}>
          <Card title="Data Health Trend (7 Days)">
            <ReactECharts option={getHealthOption()} style={{ height: 300 }} />
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="Rule Type Distribution">
            <ReactECharts option={getRuleTypeOption()} style={{ height: 300 }} />
          </Card>
        </Col>
      </Row>

      {/* Recent Executions */}
      <Card title="Recent Executions">
        <Table
          columns={executionColumns}
          dataSource={mockExecutions}
          rowKey="id"
          pagination={false}
        />
      </Card>
    </div>
  )
}

export default Dashboard
