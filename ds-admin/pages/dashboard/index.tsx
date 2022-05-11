import { useTitle } from 'ahooks'
import useAuth from 'hooks/use-auth'
import LayoutBase from 'layout/base'
import type { NextPage } from 'next'

interface DashboardProps {}

const Dashboard: NextPage = (props: DashboardProps) => {
  useTitle('控制台')

  return <LayoutBase>dashboard</LayoutBase>
}

export default Dashboard
