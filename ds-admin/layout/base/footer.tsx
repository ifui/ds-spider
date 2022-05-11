import styled from '@emotion/styled'
import type { NextPage } from 'next'

const FooterContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 2rem;
`

const Footer: NextPage = () => {
  return <FooterContainer>ifui@foxmail.com</FooterContainer>
}

export default Footer
