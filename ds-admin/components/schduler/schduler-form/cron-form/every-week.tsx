import { Form, Input, Space } from 'antd'

export default function EveryWeek() {
  return (
    <Space>
      <Form.Item name={['cron', 'week']}>
        <Input addonBefore="星期" />
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
