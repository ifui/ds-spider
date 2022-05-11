import type { NextPage } from 'next'

const HFlex: NextPage = props => {
  return (
    <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
      {props.children}
    </div>
  )
}

export default HFlex
