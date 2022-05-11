import useSWR from 'swr'
import RouterConfig from 'config/route'
import { getToken, removeToken } from '@/../utils/cookie'
import { useRouter } from 'next/router'
import { useEffect } from 'react'
import { AuthUrl, UserType } from 'api/auth'
import { Req } from 'utils/axios'
import { message } from 'antd'

interface UseAuthOptions {
  redirectTo?: string
}

/**
 * 获取认证状态，如果未认证则跳转至登录页面
 */
export default function useAuth(options?: UseAuthOptions) {
  const router = useRouter()

  // 跳转地址
  const redirectTo = options?.redirectTo
    ? '?redirect=' + encodeURIComponent(options.redirectTo)
    : '?redirect=' + encodeURIComponent(router.asPath)

  const getKey = () => {
    if (!getToken()) {
      return null
    }
    return AuthUrl.userinfo
  }

  const request = useSWR(getKey, url => Req.get<UserType>(url), {
    onError: () => {
      removeToken()
      message.error('用户信息已失效，请重新登录')
      // 跳转到登录页面，并附带当前地址
      router.push(RouterConfig.login + redirectTo)
    },
  })

  useEffect(() => {
    if (!getToken() && router.pathname !== RouterConfig.login) {
      // 跳转到登录页面，并附带当前地址
      router.push(RouterConfig.login + redirectTo)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return request.data?.data
}
