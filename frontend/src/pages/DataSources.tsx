import { useState } from 'react'
import { Table, Button, Modal, Form, Input, Select, message, Popconfirm } from 'antd'
import { PlusOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons'

const { Option } = Select

interface Datasource {
  id: number
  name: string
  type: string
  host: string
  port: number
  database: string
  is_active: boolean
}

const DataSources = () => {
  const [datasources, setDatasources] = useState<Datasource[]>([
    { id: 1, name: 'Production DB', type: 'postgresql', host: 'db.example.com', port: 5432, database: 'orders', is_active: true },
    { id: 2, name: 'Analytics DB', type: 'mysql', host: 'analytics.example.com', port: 3306, database: 'analytics', is_active: true },
    { id: 3, name: 'User Database', type: 'postgresql', host: 'users.example.com', port: 5432, database: 'users', is_active: false },
  ])
  const [modalVisible, setModalVisible] = useState(false)
  const [form] = Form.useForm()

  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'type', key: 'type', render: (type: string) => <span style={{ textTransform: 'uppercase' }}>{type}</span> },
    { title: 'Host', dataIndex: 'host', key: 'host' },
    { title: 'Port', dataIndex: 'port', key: 'port' },
    { title: 'Database', dataIndex: 'database', key: 'database' },
    {
      title: 'Status',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (active: boolean) => active ? <span style={{ color: '#52c41a' }}>Active</span> : <span style={{ color: '#999' }}>Inactive</span>
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Datasource) => (
        <Space>
          <Button type="link" size="small" icon={<EditOutlined />}>Edit</Button>
          <Popconfirm title="Delete this datasource?" onConfirm={() => handleDelete(record.id)}>
            <Button type="link" size="small" danger icon={<DeleteOutlined />}>Delete</Button>
          </Popconfirm>
        </Space>
      )
    }
  ]

  const handleDelete = (id: number) => {
    setDatasources(datasources.filter(ds => ds.id !== id))
    message.success('Datasource deleted')
  }

  const handleAdd = (values: any) => {
    const newDs: Datasource = {
      id: Math.max(...datasources.map(d => d.id)) + 1,
      ...values,
      is_active: true
    }
    setDatasources([...datasources, newDs])
    setModalVisible(false)
    form.resetFields()
    message.success('Datasource added')
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <h2>Data Sources</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
          Add Data Source
        </Button>
      </div>

      <Table columns={columns} dataSource={datasources} rowKey="id" />

      <Modal
        title="Add Data Source"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleAdd}>
          <Form.Item name="name" label="Name" rules={[{ required: true }]}>
            <Input placeholder="Production DB" />
          </Form.Item>
          <Form.Item name="type" label="Type" rules={[{ required: true }]}>
            <Select>
              <Option value="postgresql">PostgreSQL</Option>
              <Option value="mysql">MySQL</Option>
              <Option value="mongodb">MongoDB</Option>
            </Select>
          </Form.Item>
          <Form.Item name="host" label="Host" rules={[{ required: true }]}>
            <Input placeholder="localhost" />
          </Form.Item>
          <Form.Item name="port" label="Port" rules={[{ required: true }]}>
            <Input type="number" placeholder="5432" />
          </Form.Item>
          <Form.Item name="database" label="Database" rules={[{ required: true }]}>
            <Input placeholder="mydb" />
          </Form.Item>
          <Form.Item name="username" label="Username" rules={[{ required: true }]}>
            <Input placeholder="postgres" />
          </Form.Item>
          <Form.Item name="password" label="Password" rules={[{ required: true }]}>
            <Input.Password placeholder="••••••••" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default DataSources
