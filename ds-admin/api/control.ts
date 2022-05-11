export interface ControlServerType {
  id: number
  name: string
  host: string
  port: number
  username?: string
  password?: string
  to_email?: string
}

export interface ControlDaemonStatusType {
  node_name: string
  pending: number
  finished: number
  running: number
  status: string
}

export interface ControlListProjectsType {
  node_name: string
  projects: string[]
  status: string
}

export interface ControlListSpidersType {
  node_name: string
  spiders: string[]
  status: string
}

export interface ControlJobInfoType {
  project: string
  spider: string
  id: string
  start_time: string
  end_time: string
}
export interface ControlListJobsType {
  node_name: string
  status: string
  finished: ControlJobInfoType[]
  pending: ControlJobInfoType[]
  running: ControlJobInfoType[]
}

export interface ControlListVersionsType {
  status: string
  versions: string[]
}

export const controlUrl = {
  /** 爬虫服务器列表 */
  servers: '/control/servers/',
  /** 爬虫服务器状态 */
  daemonstatus: '/control/daemonstatus/',
  /** 爬虫工程列表 */
  listprojects: '/control/listprojects/',
  /** 爬虫项目列表 */
  listspiders: '/control/listspiders/',
  /** 爬虫任务列表 */
  listjobs: '/control/listjobs/',
  /** 执行爬虫任务 */
  schedule: '/control/schedule/',
  /** 取消爬虫任务 */
  cancel: '/control/cancel/',
  /** 获取某个任务的日志信息 */
  logs: '/control/logs/',
  /** 显示爬虫项目的版本 */
  listversions: '/control/listversions/',
  /** 删除爬虫项目版本 */
  delversion: '/control/delversion/',
  /** 删除一个爬虫项目 */
  delproject: '/control/delproject/',
}
