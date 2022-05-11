import {
  PauseCircleOutlined,
  PlayCircleOutlined,
  PoweroffOutlined,
  RedoOutlined,
} from '@ant-design/icons'
import { Button, Card, message, Space, Tag, Tooltip } from 'antd'
import { SchedulerStatusType, schedulerUrl } from 'api/scheduler'
import HFlex from 'components/flex/h-flex'
import Spacer from 'components/spacer'
import type { NextPage } from 'next'
import { Req } from 'utils/axios'
import useSWR, { useSWRConfig } from 'swr'

const SchedulerToolbar: NextPage = () => {
  const { mutate } = useSWRConfig()

  const { data } = useSWR(schedulerUrl.status, url =>
    Req.get<SchedulerStatusType>(url).catch(() => {
      message.error('服务状态获取失败')
    })
  )

  const handleStart = () => {
    Req.get(schedulerUrl.start)
      .then(() => {
        message.success('服务启动成功')
        mutate(schedulerUrl.status)
        mutate(schedulerUrl.get_jobs)
      })
      .catch(() => {
        message.error('服务启动失败')
      })
  }

  const handleShutdown = () => {
    Req.get(schedulerUrl.shutdown)
      .then(() => {
        message.success('服务已停止')
        mutate(schedulerUrl.status)
        mutate(schedulerUrl.get_jobs)
      })
      .catch(() => {
        message.error('服务停止失败')
      })
  }

  const handlePause = () => {
    Req.get(schedulerUrl.pause).then(() => {
      message.success('服务已暂停')
      mutate(schedulerUrl.status)
      mutate(schedulerUrl.get_jobs)
    })
  }

  const handleResume = () => {
    Req.get(schedulerUrl.resume)
      .then(() => {
        message.success('服务重启成功')
        mutate(schedulerUrl.status)
        mutate(schedulerUrl.get_jobs)
      })
      .catch(() => {
        message.error('服务重启失败')
      })
  }

  return (
    <Card>
      <HFlex>
        <Space>
          <b>定时任务</b>
          <Tag
            color={
              data?.data.status === 1
                ? 'processing'
                : data?.data.status === 2
                ? 'warning'
                : 'error'
            }
          >
            {data?.data.status === 1
              ? '运行中'
              : data?.data.status === 2
              ? '已暂停'
              : '已停止'}
          </Tag>
        </Space>
        <Spacer />
        <Space>
          <Tooltip title="启动">
            <Button onClick={handleStart} type="text" icon={<PlayCircleOutlined />} />
          </Tooltip>
          <Tooltip title="暂停">
            <Button onClick={handlePause} type="text" icon={<PauseCircleOutlined />} />
          </Tooltip>
          <Tooltip title="停止">
            <Button onClick={handleShutdown} type="text" icon={<PoweroffOutlined />} />
          </Tooltip>
          <Tooltip title="重启">
            <Button onClick={handleResume} type="text" icon={<RedoOutlined />} />
          </Tooltip>
        </Space>
      </HFlex>
    </Card>
  )
}

export default SchedulerToolbar
