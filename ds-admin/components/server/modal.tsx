import { Divider, Form, Input, InputNumber, message, Modal } from 'antd'
import { ControlServerType, controlUrl } from 'api/control'
import type { NextPage } from 'next'
import type { FieldData } from 'rc-field-form/es/interface'
import { useEffect } from 'react'
import { Req } from 'utils/axios'

export interface ServerModalOptionsType {
  type: 'add' | 'edit'
  title?: string
  initialValues?: ControlServerType
}

interface ServerModalProps {
  visible: boolean
  onCancel: () => void
  options: ServerModalOptionsType
  refresh: () => void
}

const ServerModal: NextPage<ServerModalProps> = props => {
  const [form] = Form.useForm()

  useEffect(() => {
    form && form.resetFields()
  }, [form, props.options])

  const handleSubmit = async () => {
    const isValidate = await form.validateFields()
    if (!isValidate) {
      message.error('请重新检查表单项')
      return
    }
    const values = form.getFieldsValue()

    if (props.options?.type === 'add') {
      // 添加服务器
      Req.post(controlUrl.servers, values)
        .then(() => {
          message.success('服务器创建成功')
          props.onCancel()
          props.refresh()
        })
        .catch(error => {
          message.error('服务器创建失败，请检查相关配置')
          let errors: FieldData[] = []
          for (let key in error?.data?.errorData) {
            errors.push({
              name: key,
              errors: error?.data?.errorData[key],
            })
          }
          form.setFields(errors)
        })
    } else if (props.options?.type === 'edit') {
      // 更新服务器
      if (!props.options?.initialValues?.id) {
        message.error('找不到需要更新的服务器，请重试')
        return
      }

      Req.put(controlUrl.servers + props.options?.initialValues?.id + '/', values)
        .then(() => {
          message.success('服务器更新成功')
          props.onCancel()
          props.refresh()
        })
        .catch(error => {
          message.error('服务器更新失败，请检查相关配置')
          let errors: FieldData[] = []
          for (let key in error?.data?.errorData) {
            errors.push({
              name: key,
              errors: error?.data?.errorData[key],
            })
          }
          form.setFields(errors)
        })
    }
  }

  return (
    <Modal
      title={props?.options?.title}
      visible={props?.visible}
      onCancel={props.onCancel}
      onOk={handleSubmit}
      okText="提交"
      cancelText="取消"
      getContainer={false}
      forceRender={true}
    >
      <Form
        form={form}
        initialValues={props?.options?.initialValues}
        name="server-form"
        layout="vertical"
        onFinish={handleSubmit}
      >
        <Form.Item
          label="服务器名"
          name="name"
          rules={[
            {
              required: true,
              message: '请输入服务器名',
            },
          ]}
        >
          <Input placeholder="请输入服务器名" />
        </Form.Item>

        <Form.Item
          label="主机地址"
          name="host"
          rules={[
            {
              required: true,
              message: '请输入主机地址',
            },
          ]}
        >
          <Input placeholder="127.0.0.1" />
        </Form.Item>

        <Form.Item
          label="端口"
          name="port"
          rules={[
            {
              required: true,
              message: '请输入端口',
            },
          ]}
        >
          <InputNumber placeholder="6800" />
        </Form.Item>

        <Divider>认证信息</Divider>

        <Form.Item label="用户名" name="username">
          <Input placeholder="请输入用户名" />
        </Form.Item>

        <Form.Item label="密码" name="password">
          <Input.Password placeholder="请输入密码" />
        </Form.Item>
      </Form>
    </Modal>
  )
}

export default ServerModal
