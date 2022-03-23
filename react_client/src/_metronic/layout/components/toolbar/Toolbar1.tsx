/* eslint-disable jsx-a11y/anchor-is-valid */
import clsx from 'clsx'
import React from 'react'
import {FC} from 'react'
import {KTSVG} from '../../../helpers'
import {useLayout} from '../../core'
import { Toolbar2 } from './Toolbar2'
import { Toolbar3 } from './Toolbar3'
import {ToolbarMenu} from './ToolbarMenu'

const Toolbar1: FC = () => {
  const {classes} = useLayout()

  return (
    <div className='bg-white' id='kt_toolbar'>

      <div className="d-flex flex-row-fluid"> {/*TODO: Revisar si este div hace falta */}
        <div className="d-flex flex-column flex-row-fluid">
            <div className="d-flex flex-column-fluid flex-center"> {/*TODO: Revisar si este div hace falta */}
              <div className="d-flex align-items-stretch justify-content-between flex-lg-grow-1">
                  <Toolbar2 />
              </div>
            </div>
            <div className="d-flex flex-column-fluid">
                <div
                  id='kt_toolbar_container'
                  className={clsx(classes.toolbarContainer.join(' '), 'd-flex flex-stack')}
                  style={{width:"100% !important"}}
                >
                  <div className="col-xl-1"></div>
                  <div className="col-xl-11">
                    <div
                      // className='menu menu-lg-rounded menu-column menu-lg-row menu-state-bg menu-title-gray-700 menu-state-title-primary menu-state-icon-primary menu-state-bullet-primary menu-arrow-gray-400 fw-bold my-5 my-lg-0 align-items-stretch'
                      id='#kt_header_menu'
                      data-kt-menu='true'
                    >
                      <ToolbarMenu />
                      <hr />
                    </div>
                  </div>
                  
                </div>
            </div>
         
            <div className="d-flex flex-column-fluid flex-center">
              <div className="col-xl-1"></div>
                <div className="col-xl-11">
                  <div
                    className={clsx(classes.toolbarContainer.join(' '), 'd-flex flex-stack')}
                    id='kt_toolbar_container2'
                  >
                    <Toolbar3 />
                  </div>
              </div>
            </div>
        </div>
      </div>
    </div>
  )
}

export {Toolbar1}
