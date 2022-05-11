import type { NextPage } from 'next'

const Center: NextPage = props => {
  return (
    <div
      style={{
        display: 'flex',
        width: '100%',
        height: '100%',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
      }}
    >
      {props.children}
    </div>
  )
}

export default Center
