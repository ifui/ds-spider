import { Select } from 'antd'
import { ControlServerType, controlUrl } from 'api/control'
import type { NextPage } from 'next'
import useSWR from 'swr'
import { Req } from 'utils/axios'

const ServerForm: NextPage = props => {
  const { data } = useSWR(controlUrl.servers, url => Req.get<ControlServerType[]>(url))

  return (
    <Select {...props}>
      {data?.data.map(item => (
        <Select.Option key={item.id} value={String(item.id)}>
          {item.name}
        </Select.Option>
      ))}
    </Select>
  )
}

export default ServerForm
