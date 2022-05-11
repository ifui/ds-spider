import { Form, Select } from 'antd'
import EveryDay from './every-day'
import EveryHour from './every-hour'
import EveryMonth from './every-month'
import EveryWeek from './every-week'
import NDay from './n-day'
import NHour from './n-hour'
import NMinute from './n-minute'

// 预定义的一些配置
export const cronSelectConfig = [
  {
    type: 'every_day',
    name: '每天',
    allow_field: ['hour', 'minute'],
    default_value: {
      day: '*',
    },
    render: () => <EveryDay />,
  },
  {
    type: 'n_day',
    name: 'N天',
    allow_field: ['day', 'hour', 'minute'],
    default_value: {},
    render: () => <NDay />,
  },
  {
    type: 'every_hour',
    name: '每小时',
    allow_field: ['minute'],
    default_value: {
      hour: '*',
    },
    render: () => <EveryHour />,
  },
  {
    type: 'n_hour',
    name: 'N小时',
    allow_field: ['hour', 'minute'],
    default_value: {},
    render: () => <NHour />,
  },
  {
    type: 'n_minute',
    name: 'N分钟',
    allow_field: ['minute'],
    default_value: {},
    render: () => <NMinute />,
  },
  {
    type: 'every_week',
    name: '每星期',
    allow_field: ['week', 'hour', 'minute'],
    default_value: {},
    render: () => <EveryWeek />,
  },
  {
    type: 'every_month',
    name: '每月',
    allow_field: ['day', 'hour', 'minute'],
    default_value: {
      month: '*',
    },
    render: () => <EveryMonth />,
  },
]

const CronForm = (props: { value?: string }) => {
  return (
    <>
      <Select {...props}>
        {cronSelectConfig.map(item => (
          <Select.Option key={item.name} value={item.type}>
            {item.name}
          </Select.Option>
        ))}
      </Select>

      <div style={{ marginTop: '1rem' }}>
        {cronSelectConfig.filter(item => item.type === props?.value)[0]?.render()}
      </div>
    </>
  )
}

export default CronForm
