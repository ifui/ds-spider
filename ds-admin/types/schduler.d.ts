/**
 * 定时任务参数
 */
export interface SchedulerFormInitialValues {
  project: string
  spider: string
  version?: string
  serverId: string
  cron?:
    | {
        type: string
        day: string
        hour: string
        minute: string
        week: string
      }
    | any
}
