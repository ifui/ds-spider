import {
  DeleteOutlined,
  DeploymentUnitOutlined,
  EditOutlined,
  EnterOutlined,
  MoreOutlined,
} from '@ant-design/icons'
import styled from '@emotion/styled'
import { useBoolean } from 'ahooks'
import { Col, Dropdown, Menu, message, Row, Spin, Typography } from 'antd'
import { ControlServerType, controlUrl } from 'api/control'
import Spacer from 'components/spacer'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import { Req } from 'utils/axios'

interface ServerListProps {
  data: ControlServerType[]
  handleClickEdit: (value: ControlServerType) => void
  handleDelete: (id: number) => void
}

const ServerListContainer = styled.div`
  margin: 1rem 0;
`

const LoadingContainer = styled.div`
  display: flex;
  position: absolute;
  flex-direction: column;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.06);
`

const ServerListItem = styled.div`
  display: flex;
  align-items: center;
  padding: 15px;
  user-select: none;
  background-color: #fff;
  cursor: pointer;
  border: 1px solid transparent;
  box-shadow: 0 2px 0 rgb(0 0 0 / 2%);
  transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
  &:hover {
    border: 1px solid #0788f0;
  }
`

const ServerListItemIcon = styled.div`
  background-color: #264ff7;
  border-radius: 100%;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 0.7rem;
  font-size: 1.6em;
`

const ServerList: NextPage<ServerListProps> = props => {
  const [loading, { setTrue, setFalse }] = useBoolean()

  const router = useRouter()

  const handleEnter = (id: number) => {
    setTrue()
    Req.get(controlUrl.daemonstatus + id + '/')
      .then(() => {
        message.success('连接成功')
        router.push('/control/' + id)
      })
      .catch(() => {
        message.error('服务器连接失败，请检查服务器配置')
      })
      .finally(() => {
        setFalse()
      })
  }

  return (
    <ServerListContainer>
      <Row gutter={[16, 16]}>
        {props?.data?.map(item => (
          <Col key={item.id} xs={24} sm={24} md={12} lg={8} xl={6}>
            <ServerListItem onDoubleClick={() => handleEnter(item.id)}>
              <ServerListItemIcon>
                <DeploymentUnitOutlined />
              </ServerListItemIcon>
              <div>
                <Typography>{item.name}</Typography>
                <Typography>
                  主机：{item.host} 端口：{item.port}
                </Typography>
              </div>
              <Spacer />
              <Dropdown
                overlay={
                  <Menu>
                    <Menu.Item
                      key="edit"
                      icon={<EditOutlined />}
                      onClick={() => props.handleClickEdit(item)}
                    >
                      编辑
                    </Menu.Item>
                    <Menu.Item
                      key="enter"
                      icon={<EnterOutlined />}
                      onClick={() => handleEnter(item.id)}
                    >
                      进入
                    </Menu.Item>
                    <Menu.Item
                      key="delete"
                      icon={<DeleteOutlined />}
                      onClick={() => props.handleDelete(item.id)}
                    >
                      删除
                    </Menu.Item>
                  </Menu>
                }
                trigger={['click']}
                arrow
              >
                <MoreOutlined style={{ fontSize: '1.5em' }} />
              </Dropdown>
            </ServerListItem>
          </Col>
        ))}
      </Row>

      {loading && (
        <LoadingContainer>
          <Spin />
          <div>正在连接服务器...</div>
        </LoadingContainer>
      )}
    </ServerListContainer>
  )
}

export default ServerList
