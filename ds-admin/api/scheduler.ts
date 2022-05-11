export interface SchedulerJobType {
  id: string
  args: string[]
  executor: string
  func_ref: string
  kwargs: {
    cron: {
      year: string
      month: string
      week: string
      day: string
      hour: string
      minute: string
      second: string
    }
    form: {
      project: string
      spider: string
    }
    id: string
    type: string
  }
  name: string
  pending: string
  next_run_time: string
  server_name: string
}

export interface SchedulerStatusType {
  status: 0 | 1 | 2
}

export interface SchedulerLogType {
  id: number
  duration: string
  exception: string
  finished: string
  job_id: string
  run_time: string
  status: string
  traceback?: string
}

export const schedulerUrl = {
  /** 添加一个自动执行爬虫的定时任务 */
  add_spider_job: '/scheduler/add_spider_job/',
  /** 获取定时任务列表 */
  get_jobs: '/scheduler/get_jobs/',
  /** 获取指定定时任务 */
  get_job: '/scheduler/get_job/',
  /** 修改定时任务 */
  modify_job: '/scheduler/modify_job/',
  /** 删除定时任务 */
  remove_job: '/scheduler/remove_job/',
  /** 启动定时任务 */
  start: '/scheduler/start/',
  /** 停止定时任务 */
  shutdown: '/scheduler/shutdown/',
  /** 定时任务运行状态 */
  status: '/scheduler/status/',
  /** 停止定时任务 */
  pause: '/scheduler/pause/',
  /** 重启定时任务 */
  resume: '/scheduler/resume/',
  /** 重启指定的定时任务 */
  resume_job: '/scheduler/resume_job/',
  /** 日志 */
  get_log: '/scheduler/get_log/',
}
