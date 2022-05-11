import { Alert, DatePicker, message, Modal, ModalProps } from 'antd'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import { useState } from 'react'
import type { RangeValue } from 'rc-picker/lib/interface'
import { Req } from 'utils/axios'
import { controlUrl } from 'api/control'
import moment from 'moment'

interface ProjectSpiderDateModalProps extends ModalProps {
  project: string
  spider: string
  version?: string
  onCancel: () => void
}

const ProjectSpiderDateModal: NextPage<ProjectSpiderDateModalProps> = props => {
  const { query } = useRouter()
  const [value, setValue] = useState<RangeValue<moment.Moment>>()

  const handleSubmit = () => {
    if (!query?.id || !value) return

    const start_time = value[0]?.format('YYYYMMDD')
    const end_time = value[1]?.format('YYYYMMDD')

    Req.post(controlUrl.schedule + query?.id + '/', {
      project: props.project,
      spider: props.spider,
      _version: props.version ? props.version : undefined,
      start_time,
      end_time,
    })
      .then(res => {
        message.success('任务添加成功')
        props.onCancel()
      })
      .catch(() => {
        message.error('任务添加失败')
      })
  }

  return (
    <Modal {...props} onOk={handleSubmit}>
      <Alert message="请选择采集的时间范围" type="info" showIcon />

      <DatePicker.RangePicker
        value={value}
        onChange={e => setValue(e)}
        style={{ marginTop: '1rem', width: '100%' }}
      />
    </Modal>
  )
}

export default ProjectSpiderDateModal
