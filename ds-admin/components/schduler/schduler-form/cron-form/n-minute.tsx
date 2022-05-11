import { Form, Input, Space } from 'antd'

export default function NMinute() {
  return (
    <Space>
      <Form.Item name={['cron', 'minute']}>
        <Input addonAfter="分" />
      </Form.Item>
    </Space>
  )
}
