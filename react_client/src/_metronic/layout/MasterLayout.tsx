import React, {useEffect} from 'react'
import {AsideDefault} from './components/aside/AsideDefault'
import {HeaderWrapper} from './components/header/HeaderWrapper'
import {ScrollTop} from './components/ScrollTop'
import {Content} from './components/Content'
import {PageDataProvider} from './core'
import {useLocation} from 'react-router-dom'
import {
  DrawerMessenger,
  ExploreMain,
  ActivityDrawer,
  Main,
  InviteUsers,
  UpgradePlan,
} from '../partials'
import {MenuComponent} from '../assets/ts/components'

import { Toolbar1 } from './components/toolbar/Toolbar1'


const MasterLayout: React.FC = ({children}) => {
  const location = useLocation()
  useEffect(() => {
    setTimeout(() => {
      MenuComponent.reinitialization()
    }, 500)
  }, [])

  useEffect(() => {
    setTimeout(() => {
      MenuComponent.reinitialization()
    }, 500)
  }, [location.key])

  return (
    <PageDataProvider>
      <div className='page d-flex flex-row flex-column-fluid'>
        <AsideDefault />
        <div className='wrapper d-flex flex-column flex-row-fluid' id='kt_wrapper'>
          <HeaderWrapper />
          {/* <div className="d-flex flex-row h-300px">
            <div className="d-flex flex-column flex-row-auto w-200px">
                <div className="d-flex flex-column-auto h-50px bg-primary">
                    <span className="text-white">Fixed Height</span>
                </div>

                <div className="d-flex flex-column-fluid bg-success flex-center">
                    <span className="text-white">Fluid Height</span>
                </div>
            </div>
          </div> */}
          <div id='kt_content' className='content d-flex flex-column flex-column-fluid'>
            <Toolbar1 />

            <div className='post d-flex flex-column-fluid' id='kt_post'  style={{marginTop:"120px"}}>
              <Content>{children}</Content>
            </div>
          </div>
        </div>
      </div>

      {/* begin:: Drawers */}
      <ActivityDrawer />
      <ExploreMain />
      <DrawerMessenger />
      {/* end:: Drawers */}

      {/* begin:: Modals */}
      <Main />
      <InviteUsers />
      <UpgradePlan />
      {/* end:: Modals */}
      <ScrollTop />
    </PageDataProvider>
  )
}

export {MasterLayout}