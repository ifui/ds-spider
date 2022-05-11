import { PlusOutlined, RedoOutlined } from '@ant-design/icons'
import { Button, Space } from 'antd'
import type { NextPage } from 'next'

interface ServerToolbarProps {
  refresh: () => void
  handleClickAdd: () => void
}

const ServerToolbar: NextPage<ServerToolbarProps> = props => {
  return (
    <Space style={{ marginTop: '0.5rem' }}>
      <Button icon={<RedoOutlined />} onClick={props.refresh}>
        刷新
      </Button>

      <Button icon={<PlusOutlined />} onClick={props.handleClickAdd}>
        添加服务器
      </Button>
    </Space>
  )
}

export default ServerToolbar
