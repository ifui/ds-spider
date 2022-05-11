import { SchedulerLogType, schedulerUrl } from 'api/scheduler'
import type { NextPage } from 'next'
import { Req } from 'utils/axios'
import useSWR from 'swr'
import { Collapse, message, Modal, ModalProps } from 'antd'
import moment from 'moment'
import Center from 'components/center'

interface SchedulerLogProps extends ModalProps {
  jobId?: string
}

const SchedulerLogModal: NextPage<SchedulerLogProps> = props => {
  const getKey = () => {
    if (!props.jobId) return null
    return schedulerUrl.get_log + props.jobId + '/'
  }

  const { data } = useSWR(getKey, url =>
    Req.get<SchedulerLogType[]>(url).catch(() => {
      message.error('获取定时任务日志信息失败')
    })
  )

  const CollapseLog = () => (
    <Collapse>
      {data?.data.map(item => (
        <Collapse.Panel header={`id: ${item.id}, ${item.status}`} key={item.id}>
          <p>
            <b>JOB ID：</b>
            {item.job_id}
          </p>

          <p>
            <b>启动时间：</b>
            {moment(item.run_time).format('yyyy年MM月DD日 HH时mm分ss秒')}
          </p>

          <p>
            <b>状态：</b>
            {item.status}
          </p>

          {item.exception && (
            <p>
              <b>错误信息：</b>
              {item.exception}
            </p>
          )}
        </Collapse.Panel>
      ))}
    </Collapse>
  )

  return (
    <Modal {...props}>
      {data?.data.length === 0 ? <Center>暂无日志</Center> : <CollapseLog />}
    </Modal>
  )
}

export default SchedulerLogModal
