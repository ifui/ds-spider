/**
 * Token 类型
 */
export interface TokenType {
  username: string
  id: number
  expires_in: string
  access_token: string
  token_type: string
}

export interface UserType {
  id: number
  username: string
  date_joined: string
  email: string
  first_name: string
  is_active: boolean
  is_staff: boolean
  is_superuser: boolean
  last_login?: string
  last_name: string
}

export const AuthUrl = {
  /** 用户登录 */
  login: '/login/',
  /** 用户信息 */
  userinfo: '/userinfo/',
}
