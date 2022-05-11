import { Modal, ModalProps } from 'antd'
import type { NextPage } from 'next'
import { SchedulerFormInitialValues } from 'types/schduler'
import SchdulerForm, { resetSchdulerFormData } from 'components/schduler/schduler-form'

interface SchedulerModalProps extends ModalProps {
  jobId?: string
  onFinish: (values: any) => void
}

const defaultValues: SchedulerFormInitialValues = {
  project: '',
  spider: '',
  serverId: '',
  cron: {
    type: 'every_day',
    day: '1',
    hour: '3',
    minute: '30',
    week: '3',
  },
}

const ControlProjectSpiderSchduler: NextPage<SchedulerModalProps> = props => {
  return (
    <Modal footer={false} {...props}>
      <SchdulerForm
        onFinish={values => props.onFinish(resetSchdulerFormData(values))}
        initialValues={defaultValues}
      />
    </Modal>
  )
}

export default ControlProjectSpiderSchduler
