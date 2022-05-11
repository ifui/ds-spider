import { ClockCircleOutlined, DeleteOutlined, SettingOutlined } from '@ant-design/icons'
import { useBoolean } from 'ahooks'
import {
  Button,
  Card,
  Col,
  message,
  Modal,
  Row,
  Space,
  Tabs,
  Tooltip,
  Typography,
} from 'antd'
import { ControlListProjectsType, controlUrl } from 'api/control'
import { SchedulerJobType, schedulerUrl } from 'api/scheduler'
import Spacer from 'components/spacer'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import useSWR from 'swr'
import { Req } from 'utils/axios'
import ControlProjectSpiderSchduler from './project-spider-schduler'
import ControlProjectSpiders from './project-spiders'

interface ControlProjectProps {}

const ControlProject: NextPage<ControlProjectProps> = props => {
  const { query } = useRouter()
  const [isShowProjectModal, { setFalse: closeProjectModal, setTrue: openProjectModal }] =
    useBoolean()

  const [
    isShowSchedulerModal,
    { setFalse: closeSchedulerModal, setTrue: openSchedulerModal },
  ] = useBoolean()

  const getKey = () => {
    if (!query?.id) return null

    return controlUrl.listprojects + query?.id + '/'
  }

  const { data, mutate } = useSWR(getKey, url => Req.get<ControlListProjectsType>(url))

  // 删除一个项目
  const handleDelete = (project: string) => {
    if (!data || !query?.id) return
    if (data?.data.projects.length <= 1) {
      return message.error('请至少保留一个项目')
    }

    Req.post(controlUrl.delproject + query.id + '/', {
      project,
    })
      .then(() => {
        message.success(`${project} 删除成功`)
        mutate()
      })
      .catch(() => {
        message.error(`${project} 删除失败`)
      })
  }

  // 添加一个定时任务
  const handleAddScheduler = (value: any) => {
    Req.post<SchedulerJobType>(schedulerUrl.add_spider_job, value)
      .then(res => {
        message.success(`任务添加成功，下次运行时间：${res.data.next_run_time}`)
        closeSchedulerModal()
      })
      .catch(() => {
        message.error(`任务添加失败`)
      })
  }

  return (
    <Card
      title="项目列表"
      extra={
        <Row>
          <Col xs={0} sm={0} md={24} lg={24} xl={24}>
            <Space>
              <Button onClick={openProjectModal} icon={<SettingOutlined />}>
                项目管理
              </Button>
              <Button onClick={openSchedulerModal} icon={<ClockCircleOutlined />}>
                添加定时任务
              </Button>
            </Space>
          </Col>

          <Col xs={24} sm={24} md={0} lg={0} xl={0}>
            <Space>
              <SettingOutlined onClick={openProjectModal} />

              <ClockCircleOutlined onClick={openSchedulerModal} />
            </Space>
          </Col>
        </Row>
      }
    >
      <Tabs>
        {data?.data.projects.map((item, index) => (
          <Tabs.TabPane tab={item} key={index}>
            <ControlProjectSpiders project={item} />
          </Tabs.TabPane>
        ))}
      </Tabs>

      <Modal
        title="项目管理"
        visible={isShowProjectModal}
        onCancel={closeProjectModal}
        onOk={closeProjectModal}
      >
        {data?.data.projects.map((item, index) => (
          <div key={index} style={{ display: 'flex', margin: '0.5rem 0' }}>
            <Typography.Text>{item}</Typography.Text>
            <Spacer />
            <Tooltip title="删除该项目">
              <Button
                type="text"
                icon={<DeleteOutlined />}
                onClick={() => handleDelete(item)}
                danger
              />
            </Tooltip>
          </div>
        ))}
      </Modal>

      {/* 定时任务 */}
      <ControlProjectSpiderSchduler
        title="添加定时任务"
        visible={isShowSchedulerModal}
        onCancel={closeSchedulerModal}
        onFinish={handleAddScheduler}
      />
    </Card>
  )
}

export default ControlProject
