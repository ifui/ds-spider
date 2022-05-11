import { message, Modal, ModalProps, Spin } from 'antd'
import { SchedulerJobType, schedulerUrl } from 'api/scheduler'
import type { NextPage } from 'next'
import SchdulerForm, { resetSchdulerFormData } from './schduler-form'
import useSWR from 'swr'
import { Req } from 'utils/axios'
import Center from 'components/center'

interface SchedulerModalProps extends ModalProps {
  jobId?: string
  onFinish: (values: any) => void
}

const SchedulerModal: NextPage<SchedulerModalProps> = props => {
  const getKey = () => {
    if (!props.jobId) return null
    return schedulerUrl.get_job + props.jobId + '/'
  }

  const { data } = useSWR(getKey, url =>
    Req.get<SchedulerJobType>(url).catch(() => {
      message.error('获取定时任务信息失败')
    })
  )

  return (
    <Modal footer={false} {...props}>
      {!data && (
        <Center>
          <Spin />
          加载中...
        </Center>
      )}
      {data && (
        <SchdulerForm
          onFinish={values => props.onFinish(resetSchdulerFormData(values))}
          initialValues={{
            project: data.data.kwargs.form.project,
            spider: data.data.kwargs.form.spider,
            serverId: data.data.kwargs.id,
            cron: {
              type: data.data.kwargs.type,
              ...data.data.kwargs.cron,
            },
          }}
        />
      )}
    </Modal>
  )
}

export default SchedulerModal
