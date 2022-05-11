import RouterConfig from 'config/route'
import axios from 'axios'
import { getToken, removeToken } from './cookie'

export const Req = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL,
  timeout: 5000,
})
// 添加请求拦截器
Req.interceptors.request.use(
  config => {
    const token = getToken()
    if (token && config.headers) {
      config.headers['Authorization'] = token
    }

    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 添加响应拦截器
Req.interceptors.response.use(
  response => {
    if (response.data?.data?.status === 'error') {
      // message.error(response.data?.data?.message)
      return Promise.reject(response)
    } else if (response.data.success) {
      return response.data
    } else if (response.status >= 200 && response.status < 300) {
      return response
    } else {
      return Promise.reject(response)
    }
  },
  error => {
    const { response } = error
    if (!response) {
      return Promise.reject(error)
    }

    // 取消全局消息通知
    // response?.data?.errorMessage && message.error(response.data.errorMessage)

    switch (response?.data?.errorMessage) {
      // 无权限
      case '令牌无效或已过期':
        removeToken()
        window.location.href = RouterConfig.login
        break
      default:
        break
    }
    return Promise.reject(response)
  }
)
