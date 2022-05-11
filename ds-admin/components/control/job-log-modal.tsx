import { message, Modal, Spin } from 'antd'
import { ControlJobInfoType, controlUrl } from 'api/control'
import Center from 'components/center'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import useSWR from 'swr'
import { Req } from 'utils/axios'

interface JobLogModalProps {
  visible: boolean
  setFalse: () => void
  info?: ControlJobInfoType
}

const JobLogModal: NextPage<JobLogModalProps> = props => {
  const { query } = useRouter()

  const getKey = () => {
    if (!query?.id || !props?.info) return null

    return [
      controlUrl.logs + query?.id + '/',
      {
        project: props.info.project,
        spider: props.info.spider,
        job: props.info.id,
      },
    ]
  }

  const { data, mutate, isValidating } = useSWR(
    getKey,
    (url, params) => Req.post(url as string, params),
    {
      onError: () => {
        message.error('获取日志信息失败，请重试')
      },
    }
  )

  return (
    <Modal
      title={`${props.info?.spider} - 日志`}
      visible={props.visible}
      onCancel={props.setFalse}
      onOk={() => mutate()}
      okText="刷新"
    >
      {!data || isValidating ? (
        <Center>
          <Spin />
          <p>加载中</p>
        </Center>
      ) : (
        <pre style={{ maxHeight: '30rem', overflow: 'auto' }}>{data?.data}</pre>
      )}
    </Modal>
  )
}

export default JobLogModal
