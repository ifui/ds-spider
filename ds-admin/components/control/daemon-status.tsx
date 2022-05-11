import { useTitle } from 'ahooks'
import { Card, Col, Row, Statistic, Tag, Typography } from 'antd'
import { ControlDaemonStatusType, controlUrl } from 'api/control'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import { Req } from 'utils/axios'
import useSWR from 'swr'

interface ControlDaemonStatusProps {}

const ControlDaemonStatus: NextPage<ControlDaemonStatusProps> = props => {
  const { query } = useRouter()

  const getKey = () => {
    if (!query?.id) return null

    return controlUrl.daemonstatus + query.id + '/'
  }

  const { data } = useSWR(getKey, url => Req.get<ControlDaemonStatusType>(url), {
    // 1 秒轮询1次
    refreshInterval: 1000,
  })

  useTitle('服务器详情 - ' + data?.data.node_name)

  return (
    <Card>
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Typography.Text>
            服务器名：
            <Tag>{data?.data.node_name}</Tag>
          </Typography.Text>
        </Col>
        <Col span={8}>
          <Statistic title="运行中" value={data?.data.running || 0} />
        </Col>
        <Col span={8}>
          <Statistic title="等待中" value={data?.data.pending || 0} />
        </Col>
        <Col span={8}>
          <Statistic title="已完成" value={data?.data.finished || 0} />
        </Col>
      </Row>
    </Card>
  )
}

export default ControlDaemonStatus
