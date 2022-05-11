import { Select } from 'antd'
import { ControlListSpidersType, controlUrl } from 'api/control'
import useAntdForm from 'hooks/use-antd-form'
import type { NextPage } from 'next'
import useSWR from 'swr'
import { SchedulerFormInitialValues } from 'types/schduler'
import { Req } from 'utils/axios'

interface SpiderFormProps {}

const SpiderForm: NextPage<SpiderFormProps> = props => {
  const { values, form } = useAntdForm<SchedulerFormInitialValues>()

  const getKey = () => {
    if (!values?.serverId) return null

    return [
      controlUrl.listspiders + values?.serverId + '/',
      {
        project: values?.project,
      },
    ]
  }

  const { data, error } = useSWR(
    getKey,
    (url, params) => Req.post<ControlListSpidersType>(url as string, params),
    {
      onError: () => {
        form.setFieldsValue({
          spider: '',
        })
      },
    }
  )

  return (
    <Select {...props} disabled={!!error}>
      {data?.data.spiders.map(item => (
        <Select.Option key={item} value={String(item)}>
          {item}
        </Select.Option>
      ))}
    </Select>
  )
}

export default SpiderForm
