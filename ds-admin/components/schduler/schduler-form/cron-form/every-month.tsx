import { Form, Input, Space } from 'antd'

export default function EveryMonth() {
  return (
    <Space>
      <Form.Item name={['cron', 'day']}>
        <Input addonAfter="日" />
      </Form.Item>

      <Form.Item name={['cron', 'hour']}>
        <Input addonAfter="时" />
      </Form.Item>

      <Form.Item name={['cron', 'minute']}>
        <Input addonAfter="分" />
      </Form.Item>
    </Space>
  )
}
