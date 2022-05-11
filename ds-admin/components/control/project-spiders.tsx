import { CalendarOutlined, PlayCircleOutlined } from '@ant-design/icons'
import styled from '@emotion/styled'
import { useBoolean } from 'ahooks'
import { Button, Divider, message, Space, Spin, Tooltip } from 'antd'
import { ControlListSpidersType, controlUrl } from 'api/control'
import Center from 'components/center'
import Spacer from 'components/spacer'
import type { NextPage } from 'next'
import { useRouter } from 'next/router'
import { useState } from 'react'
import useSWR from 'swr'
import { Req } from 'utils/axios'
import ProjectSpiderDateModal from './project-spider-date-modal'
import ControlProjectSpiderVersion from './project-spider-version'

interface ControlProjectListProps {
  project: string
}

const ListItem = styled.div`
  display: flex;
  width: 100%;
  align-items: center;
  padding: 10px 5px;
  transition: background-color 0.2s;
  border-radius: 7px;
  &:hover {
    background-color: #ebeef0;
  }
`

const ControlProjectSpiders: NextPage<ControlProjectListProps> = props => {
  const { query } = useRouter()

  const [isShowDateModal, { setTrue: openDateModal, setFalse: closeDateModal }] =
    useBoolean()

  const [version, setVersion] = useState<string | undefined>(undefined)
  const [spider, setSpider] = useState('')

  const getKey = () => {
    if (!query?.id) return null
    return [
      controlUrl.listspiders + query?.id + '/',
      {
        project: props.project,
      },
    ]
  }

  const { data } = useSWR(getKey, (url, params) =>
    Req.post<ControlListSpidersType>(url as string, params).catch(() => {
      message.error('获取爬虫列表失败')
    })
  )

  // 启动爬虫
  const handleStart = (spider: string) => {
    Req.post(controlUrl.schedule + query?.id + '/', {
      project: props.project,
      spider: spider,
      _version: version ? version : undefined,
    })
      .then(() => {
        message.success('启动成功')
      })
      .catch(() => {
        message.error('启动失败')
      })
  }

  if (!data || !query?.id) {
    return (
      <div>
        {!data && (
          <Center>
            <Spin />
            加载中...
          </Center>
        )}
      </div>
    )
  }

  return (
    <div>
      {data?.data.spiders.map(item => (
        <ListItem key={item}>
          <span style={{ marginLeft: '0.5rem' }}>{item}</span>
          <Spacer />
          <Space>
            <Tooltip title="启动">
              <Button
                shape="circle"
                type="text"
                icon={<PlayCircleOutlined />}
                onClick={() => handleStart(item)}
              />
            </Tooltip>
            <Tooltip title="选择采集时间范围">
              <Button
                shape="circle"
                type="text"
                icon={<CalendarOutlined />}
                onClick={() => {
                  setSpider(item)
                  openDateModal()
                }}
              />
            </Tooltip>
          </Space>
        </ListItem>
      ))}
      <Divider />
      <div>
        {/* 版本管理 */}
        <ControlProjectSpiderVersion
          project={props.project}
          version={version || 'latest'}
          setVersion={setVersion}
        />

        <ProjectSpiderDateModal
          title="择时启动"
          project={props.project}
          spider={spider}
          version={version}
          visible={isShowDateModal}
          onCancel={closeDateModal}
        />
      </div>
    </div>
  )
}

export default ControlProjectSpiders
