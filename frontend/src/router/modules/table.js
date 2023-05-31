/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const tableRouter = {
  path: '/table',
  component: Layout,
  redirect: '/table/complex-table',
  name: 'Table',
  meta: {
    title: '通行管理',
    icon: 'table'
  },
  children: [
    {
      path: 'complex-table',
      component: () => import('@/views/table/complex-table'),
      name: '车辆权限',
      meta: { title: '车辆权限' }
    },
    {
      path: 'complex-table-records',
      component: () => import('@/views/table/complex-table-records'),
      name: '识别记录',
      meta: { title: '识别记录' }
    }
  ]
}
export default tableRouter
