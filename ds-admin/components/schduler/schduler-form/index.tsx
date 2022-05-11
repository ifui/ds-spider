import { Button, Divider, Form, FormProps, Space } from 'antd'
import HFlex from 'components/flex/h-flex'
import Spacer from 'components/spacer'
import { AntdFormProvider } from 'context/antd-form-context'
import type { NextPage } from 'next'
import { SchedulerFormInitialValues } from 'types/schduler'
import CronForm, { cronSelectConfig } from './cron-form'
import ProjectForm from './project-form'
import ServerForm from './server-form'
import SpiderForm from './spider-form'

// 整理数据
export const resetSchdulerFormData = (values: SchedulerFormInitialValues) => {
  const cronFields = cronSelectConfig.filter(item => item.type === values.cron.type)[0]

  let allowFiedls: any = {}
  cronFields.allow_field.forEach(item => {
    allowFiedls[item] = values.cron[item]
  })
  allowFiedls = { ...allowFiedls, ...cronFields.default_value }

  return {
    id: values.serverId,
    form: {
      project: values.project,
      spider: values.spider,
    },
    cron: allowFiedls,
    type: values.cron.type,
  }
}

const SchdulerForm: NextPage<FormProps> = props => {
  return (
    <AntdFormProvider name="scheduler-form" layout="vertical" {...props}>
      <Form.Item label="服务器" name="serverId" rules={[{ required: true }]}>
        <ServerForm />
      </Form.Item>

      <Form.Item label="项目" name="project" rules={[{ required: true }]}>
        <ProjectForm />
      </Form.Item>

      <Form.Item label="任务" name="spider" rules={[{ required: true }]}>
        <SpiderForm />
      </Form.Item>

      <Divider>执行周期</Divider>

      <Form.Item name={['cron', 'type']}>
        <CronForm />
      </Form.Item>

      <Divider />

      <HFlex>
        <Spacer />
        <Space>
          <Button type="primary" htmlType="submit">
            提交
          </Button>
        </Space>
      </HFlex>
    </AntdFormProvider>
  )
}

export default SchdulerForm
