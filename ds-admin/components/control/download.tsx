import { CloudDownloadOutlined } from '@ant-design/icons'
import { useBoolean } from 'ahooks'
import { Alert, Button, Card, Col, DatePicker, message, Row, Space, Switch } from 'antd'
import { FileUrl } from 'api/file'
import type { NextPage } from 'next'
import { useState } from 'react'
import { Req } from 'utils/axios'
import moment from 'moment'
import { saveAs } from 'file-saver'
import type { RangeValue } from 'rc-picker/lib/interface'

interface ControlJobDownloadProps {}

const createFileName = (values: RangeValue<moment.Moment>) => {
  let filename = 'ds.zip'
  if (!values) return filename

  if (values[0] === values[1]) {
    filename = values[0]?.format('YYYYMMDD') + '.zip'
  } else {
    filename =
      values[0]?.format('YYYYMMDD') + '_' + values[1]?.format('YYYYMMDD') + '.zip'
  }
  return filename
}

const ControlDownload: NextPage<ControlJobDownloadProps> = props => {
  const nowDate = moment()

  const [values, setValues] = useState<RangeValue<moment.Moment>>([nowDate, nowDate])
  const [loading, { setTrue, setFalse }] = useBoolean()
  const [tencentLoading, setTencentLoading] = useState(false)
  const [isOverwrite, setIsOverwrite] = useState(true)
  const [tencentDownload, setTencentDownload] = useState({
    url: '',
    expired: 0,
  })

  // 服务器本地下载
  const handleDownlad = () => {
    setTrue()

    if (!values) return

    Req.post(
      FileUrl.download,
      {
        start_time: values[0]?.format('YYYYMMDD'),
        end_time: values[1]?.format('YYYYMMDD'),
        is_overwrite: isOverwrite,
      },
      {
        timeout: 60000,
        responseType: 'blob',
      }
    )
      .then(res => {
        const filename = createFileName(values)
        saveAs(res.data, filename)
      })
      .catch(() => {
        message.error('下载失败，请联系管理员')
      })
      .finally(() => {
        setFalse()
      })
  }

  // 腾讯云服务器下载
  const handleTencentDownlad = () => {
    setTencentLoading(true)

    if (!values) return

    Req.post(
      FileUrl.tencent_download,
      {
        start_time: values[0]?.format('YYYYMMDD'),
        end_time: values[1]?.format('YYYYMMDD'),
        is_overwrite: isOverwrite,
      },
      {
        timeout: 60000,
      }
    )
      .then(res => {
        setTencentDownload(res.data)
      })
      .catch(() => {
        message.error('获取腾讯云存储下载地址失败，请联系管理员')
      })
      .finally(() => {
        setTencentLoading(false)
      })
  }

  return (
    <Card title="数据包下载">
      <Row gutter={[16, 16]}>
        {tencentDownload.url && (
          <Col span="24">
            <Alert
              type="info"
              message={
                <>
                  <b>腾讯云下载地址：</b>
                  <a href={tencentDownload.url} target="_blank" rel="noreferrer">
                    点击下载
                  </a>
                  <span>（过期时间：{tencentDownload.expired}秒）</span>
                </>
              }
            />
          </Col>
        )}

        <Col span="24">
          <b>选择日期范围：</b>
        </Col>

        <Col span="24">
          <DatePicker.RangePicker value={values} onChange={e => setValues(e)} />
        </Col>

        <Col span="24">
          <b>文件下载方式：</b>
        </Col>

        <Col span="24">
          <Space>
            <Button
              loading={loading}
              onClick={handleDownlad}
              icon={<CloudDownloadOutlined />}
            >
              本地下载
            </Button>

            <Button
              loading={tencentLoading}
              onClick={handleTencentDownlad}
              icon={<CloudDownloadOutlined />}
            >
              腾讯云下载
            </Button>
          </Space>
        </Col>

        <Col span="24">
          <Space>
            <b>文件覆盖下载：</b>
            <Switch checked={isOverwrite} onChange={e => setIsOverwrite(e)} />
          </Space>
        </Col>
      </Row>
    </Card>
  )
}

export default ControlDownload
