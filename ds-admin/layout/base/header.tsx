import styled from '@emotion/styled'
import { Avatar, Dropdown, Menu, message, Row, Space } from 'antd'
import Spacer from 'components/spacer'
import AppConfig from 'config/app'
import type { NextPage } from 'next'
import {
  DeploymentUnitOutlined,
  FieldTimeOutlined,
  LogoutOutlined,
} from '@ant-design/icons'
import { removeToken } from 'utils/cookie'
import { useRouter } from 'next/router'
import RouterConfig from 'config/route'
import useAuth from 'hooks/use-auth'
import Link from 'next/link'

const HeaderContainer = styled(Row)`
  display: flex;
  flex-direction: row;
  align-items: center;
  min-height: 3.5rem;
  box-shadow: 0px 2px 3px 0px rgb(0 0 0 / 10%);
  padding: 0.7rem;
`

const HOptionMenu = styled(Menu)`
  border-bottom: none;
`

const AppName = styled.div`
  font-weight: 700;
  margin-left: 0.5rem;
  cursor: pointer;
`

const options = [
  {
    title: '服务器列表',
    href: '/server',
    icon: <DeploymentUnitOutlined />,
  },
  {
    title: '定时任务',
    href: '/scheduler',
    icon: <FieldTimeOutlined />,
  },
]

const Header: NextPage = () => {
  const router = useRouter()
  const user = useAuth()

  // 登出
  const logout = () => {
    message.success('已登出')
    removeToken()
    router.push(RouterConfig.login)
  }

  const userMenu = (
    <Menu>
      <Menu.Item key="0" icon={<LogoutOutlined />} onClick={logout}>
        登出
      </Menu.Item>
    </Menu>
  )

  return (
    <HeaderContainer>
      <img src={AppConfig.logo} alt="logo" width={25} height={25} />
      <Link href={'/'} passHref>
        <AppName>{AppConfig.appName}</AppName>
      </Link>

      <Spacer />

      <Space>
        <HOptionMenu mode="horizontal" selectedKeys={[router.route]}>
          {options.map(item => (
            <Menu.Item key={item.href} icon={item.icon}>
              <Link href={item.href} shallow>
                {item.title}
              </Link>
            </Menu.Item>
          ))}
        </HOptionMenu>

        <Dropdown overlay={userMenu} trigger={['click']} arrow>
          <Avatar shape="square">{user?.username}</Avatar>
        </Dropdown>
      </Space>
    </HeaderContainer>
  )
}

export default Header
