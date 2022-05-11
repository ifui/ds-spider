import {
  CheckCircleOutlined,
  ClockCircleOutlined,
  CloseCircleOutlined,
  FileSearchOutlined,
  SyncOutlined,
} from '@ant-design/icons'
import { useBoolean } from 'ahooks'
import { Button, Card, message, Space, Table, Tag, Tooltip } from 'antd'
import { ColumnsType } from 'antd/lib/table'
import { ControlJobInfoType, ControlListJobsType, controlUrl } from 'api/control'
import moment from 'moment'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import { useState } from 'react'
import useSWR from 'swr'
import { Req } from 'utils/axios'
import JobLogModal from './job-log-modal'

interface ControlJobProps {}

/** 整理数据 */
const resetData = (data: ControlJobInfoType[], status: string) => {
  return data?.map(data => ({
    ...data,
    status: status,
    start_time: moment(data.start_time).format('YYYY-MM-DD HH:mm:ss'),
    end_time: moment(data.end_time).format('YYYY-MM-DD HH:mm:ss'),
  }))
}

const renderStatus = (status: string) => {
  switch (status) {
    case 'running':
      return (
        <Tag icon={<SyncOutlined spin />} color="processing">
          运行中
        </Tag>
      )
    case 'finished':
      return (
        <Tag icon={<CheckCircleOutlined />} color="success">
          已完成
        </Tag>
      )
    case 'pending':
      return (
        <Tag icon={<ClockCircleOutlined />} color="default">
          等待中
        </Tag>
      )
  }
}

const ControlJob: NextPage<ControlJobProps> = props => {
  const { query } = useRouter()
  const [visible, { setTrue, setFalse }] = useBoolean()
  const [logInfo, setLogInfo] = useState<ControlJobInfoType | undefined>(undefined)

  const getKey = () => {
    if (!query?.id) return null

    return controlUrl.listjobs + query?.id + '/'
  }

  const { data } = useSWR(getKey, url => Req.post<ControlListJobsType>(url), {
    // 轮询
    refreshInterval: 1000,
  })

  // 根据时间倒序
  const sortData = [
    ...resetData(data?.data.pending || [], 'pending'),
    ...resetData(data?.data.running || [], 'running'),
    ...resetData(data?.data.finished || [], 'finished'),
  ].sort((a, b) => {
    return moment(b.start_time).diff(a.start_time)
  })

  // 取消爬虫任务
  const handleCancel = (item: ControlJobInfoType) => {
    if (!query?.id) return

    Req.post(controlUrl.cancel + query.id + '/', {
      project: item.project,
      job: item.id,
    })
      .then(res => {
        if (res.data.status === 'ok') {
          message.success('任务已停止')
        } else {
          message.error('停止失败')
        }
      })
      .catch(() => {
        message.error('任务操作失败')
      })
  }

  // 表格项配置
  const columns: ColumnsType<ControlJobInfoType & { status: string }> = [
    {
      title: '项目',
      dataIndex: 'project',
      key: 'project',
    },
    {
      title: '任务',
      dataIndex: 'spider',
      key: 'spider',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: val => renderStatus(val),
    },
    {
      title: '开始时间',
      dataIndex: 'start_time',
      key: 'start_time',
      ellipsis: true,
    },
    {
      title: '结束时间',
      dataIndex: 'end_time',
      key: 'end_time',
      ellipsis: true,
    },
    {
      title: '操作',
      render: (_, record) => (
        <Space>
          <Tooltip title="取消任务">
            <Button
              type="text"
              icon={<CloseCircleOutlined />}
              onClick={() => handleCancel(record)}
              disabled={record.status === 'finished'}
            />
          </Tooltip>
          <Tooltip title="查看日志">
            <Button
              type="text"
              icon={<FileSearchOutlined />}
              onClick={() => {
                setLogInfo(record)
                setTrue()
              }}
            />
          </Tooltip>
        </Space>
      ),
    },
  ]

  return (
    <Card title="任务列表">
      <Table
        scroll={{ x: true }}
        loading={!data}
        rowKey="id"
        dataSource={sortData}
        columns={columns}
      />
      <JobLogModal visible={visible} setFalse={setFalse} info={logInfo} />
    </Card>
  )
}

export default ControlJob
