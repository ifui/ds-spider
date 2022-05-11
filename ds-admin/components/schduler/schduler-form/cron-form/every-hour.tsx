import { Form, Input, Space } from 'antd'

export default function EveryHour() {
  return (
    <Space>
      <Form.Item name={['cron', 'minute']}>
        <Input addonAfter="分" />
      </Form.Item>
    </Space>
  )
}
