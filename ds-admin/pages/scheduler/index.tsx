import { useTitle } from 'ahooks'
import SchedulerTable from 'components/schduler/table'
import SchedulerToolbar from 'components/schduler/toobar'
import LayoutBase from 'layout/base'
import type { NextPage } from 'next'

const Scheduler: NextPage = () => {
  useTitle('定时任务')

  return (
    <LayoutBase>
      <div style={{ marginTop: '0.3rem' }}>
        <SchedulerToolbar />
      </div>

      <div style={{ marginTop: '1rem' }}>
        <SchedulerTable />
      </div>
    </LayoutBase>
  )
}

export default Scheduler
