import { Button, Card, message, Space, Table, Tooltip } from 'antd'
import { ColumnsType } from 'antd/lib/table'
import { SchedulerJobType, schedulerUrl } from 'api/scheduler'
import type { NextPage } from 'next'
import { Req } from 'utils/axios'
import useSWR from 'swr'
import { DeleteOutlined, EditOutlined, FileSearchOutlined } from '@ant-design/icons'
import { useBoolean } from 'ahooks'
import { useState } from 'react'
import { SchedulerFormInitialValues } from 'types/schduler'
import SchedulerModal from 'components/schduler/scheduler-modal'
import SchedulerLogModal from 'components/schduler/scheduler-log-modal'

const SchedulerTable: NextPage = () => {
  const [
    isShowSchedulerModal,
    { setTrue: openSchedulerModal, setFalse: closeSchedulerModal },
  ] = useBoolean()

  const [isShowLogodal, { setTrue: openLogModal, setFalse: closeLogModal }] = useBoolean()

  const [jobId, setJobId] = useState<string | undefined>()

  const { data, mutate } = useSWR(schedulerUrl.get_jobs, url =>
    Req.get<SchedulerJobType[]>(url).catch(() => {
      message.error('获取定时任务列表失败')
    })
  )

  // 删除任务
  const handleDelete = (jobId: string) => {
    Req.delete(schedulerUrl.remove_job + jobId + '/')
      .then(() => {
        message.success('删除成功')
        mutate()
      })
      .catch(() => {
        message.error('删除失败')
      })
  }

  // 编辑定时任务
  const handleEdit = (value: SchedulerFormInitialValues) => {
    console.log(value)
    Req.put(schedulerUrl.modify_job + jobId + '/', value)
      .then(res => {
        message.success(`任务更新成功，下次运行时间：${res.data.next_run_time}`)
        mutate()
        closeSchedulerModal()
      })
      .catch(() => {
        message.error('任务更新失败')
      })
  }

  const columns: ColumnsType<SchedulerJobType> = [
    {
      title: '服务器',
      dataIndex: 'server_name',
      key: 'id',
    },
    {
      title: '项目',
      dataIndex: ['kwargs', 'form', 'project'],
      key: 'id',
    },
    {
      title: '任务',
      dataIndex: ['kwargs', 'form', 'spider'],
      key: 'id',
    },
    {
      title: '下次运行时间',
      dataIndex: 'next_run_time',
      key: 'id',
    },
    {
      title: '配置',
      dataIndex: ['kwargs', 'cron'],
      key: 'id',
      render: value => JSON.stringify(value),
    },
    {
      title: '操作',
      render: (_, record) => (
        <Space>
          <Tooltip title="编辑计划任务">
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => {
                setJobId(record.id)
                openSchedulerModal()
              }}
            />
          </Tooltip>

          <Tooltip title="查看日志">
            <Button
              type="text"
              icon={<FileSearchOutlined />}
              onClick={() => {
                setJobId(record.id)
                openLogModal()
              }}
            />
          </Tooltip>

          <Tooltip title="删除计划任务">
            <Button
              type="text"
              icon={<DeleteOutlined />}
              onClick={() => handleDelete(record.id)}
            />
          </Tooltip>
        </Space>
      ),
    },
  ]

  return (
    <Card>
      <Table rowKey="id" scroll={{ x: true }} columns={columns} dataSource={data?.data} />
      <SchedulerModal
        title="更新任务"
        visible={isShowSchedulerModal}
        onCancel={closeSchedulerModal}
        jobId={jobId}
        onFinish={handleEdit}
      />

      <SchedulerLogModal
        title="查看日志"
        visible={isShowLogodal}
        onCancel={closeLogModal}
        jobId={jobId}
      />
    </Card>
  )
}

export default SchedulerTable
