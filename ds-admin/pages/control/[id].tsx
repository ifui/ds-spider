import ControlDaemonStatus from 'components/control/daemon-status'
import ControlDownload from 'components/control/download'
import ControlJob from 'components/control/job'
import ControlProject from 'components/control/project'
import LayoutBase from 'layout/base'
import type { NextPage } from 'next'

const ControlPage: NextPage = () => {
  return (
    <LayoutBase bg="#eaeff0">
      <div style={{ marginTop: '0.5rem' }}>
        <ControlDaemonStatus />
      </div>
      <div style={{ marginTop: '1rem' }}>
        <ControlProject />
      </div>
      <div style={{ marginTop: '1rem' }}>
        <ControlDownload />
      </div>
      <div style={{ marginTop: '1rem' }}>
        <ControlJob />
      </div>
    </LayoutBase>
  )
}

export default ControlPage
