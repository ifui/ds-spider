import { DeleteOutlined } from '@ant-design/icons'
import { useBoolean } from 'ahooks'
import {
  Button,
  Dropdown,
  Menu,
  message,
  Modal,
  Space,
  Tag,
  Tooltip,
  Typography,
} from 'antd'
import { ControlListVersionsType, controlUrl } from 'api/control'
import Spacer from 'components/spacer'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import useSWR from 'swr'
import { Req } from 'utils/axios'

interface ControlProjectSpiderVersionProps {
  version: string
  project: string
  setVersion: (value: string) => void
}

const ControlProjectSpiderVersion: NextPage<ControlProjectSpiderVersionProps> = props => {
  const { query } = useRouter()
  const [visible, { setTrue, setFalse }] = useBoolean()

  const getKey = () => {
    if (!query?.id) return null

    return [
      controlUrl.listversions + query?.id + '/',
      {
        project: props.project,
      },
    ]
  }

  const { data, mutate } = useSWR(getKey, (url, params) =>
    Req.post<ControlListVersionsType>(url as string, params).catch(() => {
      message.error('获取版本列表失败')
    })
  )

  // 删除版本号
  const handleDeleteVersion = (project: string, version: string) => {
    if (!data || !query?.id) return
    if (data?.data.versions.length <= 1) {
      return message.error('请至少保留一个版本')
    }

    Req.post(controlUrl.delversion + query.id + '/', {
      project,
      version,
    })
      .then(() => {
        message.success(`${project} 的版本：${version} 删除成功`)
        mutate()
      })
      .catch(() => {
        message.error(`${project} 的版本：${version} 删除失败`)
      })
  }

  return (
    <div style={{ display: 'flex' }}>
      <Space>
        <Typography.Text>切换版本号</Typography.Text>

        {data?.data.versions.length === 0 || !data ? (
          <Tag>暂无版本号</Tag>
        ) : (
          <Dropdown
            overlay={
              <Menu>
                {data?.data.versions.map(item => (
                  <Menu.Item key={item} onClick={() => props.setVersion(item)}>
                    {item}
                  </Menu.Item>
                ))}
              </Menu>
            }
          >
            <Tag>{props.version}</Tag>
          </Dropdown>
        )}
      </Space>
      <Spacer />
      <Button onClick={setTrue}>版本管理</Button>

      <Modal visible={visible} onCancel={setFalse} title="版本管理" onOk={setFalse}>
        {data?.data.versions.map(item => (
          <div style={{ display: 'flex', margin: '0.5rem 0' }} key={item}>
            <Typography.Text>{item}</Typography.Text>
            <Spacer />
            <Tooltip title="删除该版本">
              <Button
                type="text"
                icon={<DeleteOutlined />}
                onClick={() => handleDeleteVersion(props.project, item)}
                danger
              />
            </Tooltip>
          </div>
        ))}
      </Modal>
    </div>
  )
}

export default ControlProjectSpiderVersion
