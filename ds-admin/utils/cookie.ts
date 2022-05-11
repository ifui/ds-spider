import Cookies from 'js-cookie'

// token
const TOKEN_NAME = 'token'
export const setToken = (value: string, expires: Date) =>
  Cookies.set(TOKEN_NAME, value, { expires })
export const getToken = () => Cookies.get(TOKEN_NAME)
export const removeToken = () => Cookies.remove(TOKEN_NAME)
