import type { NextPage } from 'next'
import React from 'react'
import useAuth from 'hooks/use-auth'
import styled from '@emotion/styled'
import Header from './header'
import Footer from './footer'

const LayoutContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 100%;
`

const LayoutContent = styled.div`
  position: relative;
  flex: 1;
  padding: 0.7rem;
`

interface LayoutBaseProps {
  bg?: string
}

const LayoutBase: NextPage<LayoutBaseProps> = props => {
  useAuth()

  return (
    <LayoutContainer>
      <Header />
      <LayoutContent style={{ background: props.bg }}>{props.children}</LayoutContent>
      <Footer />
    </LayoutContainer>
  )
}

export default LayoutBase
