import type { NextPage } from 'next'

const VFlex: NextPage = props => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      {props.children}
    </div>
  )
}

export default VFlex
