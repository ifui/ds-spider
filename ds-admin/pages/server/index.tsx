import { useBoolean, useTitle } from 'ahooks'
import { message, Skeleton } from 'antd'
import { ControlServerType, controlUrl } from 'api/control'
import LayoutBase from 'layout/base'
import { useState } from 'react'
import { Req } from 'utils/axios'

import ServerList from '../../components/server/list'

import type { NextPage } from 'next'
import useSWR from 'swr'
import ServerModal, { ServerModalOptionsType } from 'components/server/modal'
import ServerToolbar from 'components/server/toolbar'

const ServerPage: NextPage = () => {
  useTitle('服务器列表')

  const [visible, { setTrue, setFalse }] = useBoolean()

  const { data, mutate } = useSWR(controlUrl.servers, url =>
    Req.get<ControlServerType[]>(url)
  )

  const [modalOptions, setModalOptions] = useState<ServerModalOptionsType>({
    type: 'add',
  })

  const handleClickAdd = () => {
    setModalOptions({
      type: 'add',
      title: '添加服务器',
    })
    setTrue()
  }

  const handleClickEdit = (value: ControlServerType) => {
    setModalOptions({
      type: 'edit',
      title: '编辑服务器',
      initialValues: value,
    })
    setTrue()
  }

  const handleDelete = (id: number) => {
    Req.delete(controlUrl.servers + id + '/').then(res => {
      message.success('删除成功')
      mutate()
    })
  }

  return (
    <LayoutBase bg="#eaeff0">
      <ServerToolbar refresh={mutate} handleClickAdd={handleClickAdd} />
      {data && data?.data ? (
        <ServerList
          data={data.data}
          handleClickEdit={handleClickEdit}
          handleDelete={handleDelete}
        />
      ) : (
        <Skeleton />
      )}
      <ServerModal
        refresh={mutate}
        visible={visible}
        onCancel={setFalse}
        options={modalOptions}
      />
    </LayoutBase>
  )
}

export default ServerPage
