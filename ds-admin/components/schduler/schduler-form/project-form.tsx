import { message, Select } from 'antd'
import { ControlListProjectsType, controlUrl } from 'api/control'
import useAntdForm from 'hooks/use-antd-form'
import type { NextPage } from 'next'
import useSWR from 'swr'
import { SchedulerFormInitialValues } from 'types/schduler'
import { Req } from 'utils/axios'

interface ProjectFormProps {}

const ProjectForm: NextPage<ProjectFormProps> = props => {
  const { values, form } = useAntdForm<SchedulerFormInitialValues>()

  const getKey = () => {
    if (!values?.serverId) return null

    return controlUrl.listprojects + values?.serverId + '/'
  }

  const { data, error } = useSWR(getKey, url => Req.get<ControlListProjectsType>(url), {
    onError: () => {
      message.error('获取项目列表失败，请检查该服务器连接是否正常')
      form.setFieldsValue({
        project: '',
      })
    },
  })

  return (
    <Select {...props} disabled={!!error}>
      {data?.data.projects.map(item => (
        <Select.Option key={item} value={String(item)}>
          {item}
        </Select.Option>
      ))}
    </Select>
  )
}

export default ProjectForm
