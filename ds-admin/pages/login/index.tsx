import { useBoolean, useTitle } from 'ahooks'
import { Button, Checkbox, Form, Input, message } from 'antd'
import { AuthUrl, TokenType } from 'api/auth'
import AppConfig from 'config/app'
import LoginConfig from 'config/login'
import moment from 'moment'
import { useRouter } from 'next/router'
import { Req } from 'utils/axios'
import { removeToken, setToken } from 'utils/cookie'

import styled from '@emotion/styled'

import type { NextPage } from 'next'
const LoginContainer = styled.div`
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
  background-image: url('${LoginConfig.loginBg}');
`

const LoginBox = styled.div`
  width: 20rem;
`

interface LoginParams {
  username: string
  password: string
  remember: boolean
}

const LoginPage: NextPage = () => {
  useTitle('后台登录')
  const [isSubmit, { setTrue, setFalse }] = useBoolean()
  const router = useRouter()

  const handleLogin = (values: LoginParams) => {
    setTrue()

    Req.post<TokenType>(AuthUrl.login, {
      username: values.username,
      password: values.password,
    })
      .then(res => {
        // 设置 TOKEN 到 cookie 中
        setToken('Bearer ' + res.data.access_token, moment(res.data.expires_in).toDate())
        // 跳转页面
        router.push((router.query?.redirect as string) || '/server')
        message.success('登录成功')
      })
      .catch(res => {
        message.error('登录失败，请检查用户名密码')
        removeToken()
      })
      .finally(() => setFalse())
  }

  return (
    <LoginContainer>
      <LoginBox>
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <img src={AppConfig.logo} alt="logo" width="80" height="80" />
        </div>

        <Form
          name="login-form"
          autoComplete="off"
          onFinish={handleLogin}
          layout="vertical"
        >
          <Form.Item
            label="用户名"
            name="username"
            rules={[
              {
                required: true,
                message: '请输入用户名',
              },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="密码"
            name="password"
            rules={[
              {
                required: true,
                message: '请输入密码',
              },
            ]}
          >
            <Input.Password />
          </Form.Item>
          <Form.Item name="remember" valuePropName="checked">
            <Checkbox>记住我</Checkbox>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={isSubmit} block>
              登录
            </Button>
          </Form.Item>
        </Form>
      </LoginBox>
    </LoginContainer>
  )
}

export default LoginPage
