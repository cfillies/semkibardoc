/* eslint-disable jsx-a11y/anchor-is-valid */
import clsx from 'clsx'
import {FC} from 'react'
import {KTSVG} from '../../../helpers'
import {useLayout} from '../../core'
import { Toolbar2 } from './Toolbar2'
import { Toolbar3 } from './Toolbar3'
import {ToolbarMenu} from './ToolbarMenu'

const Toolbar1: FC = () => {
  const {classes} = useLayout()

  return (
    <div className='toolbar' id='kt_toolbar'>

      <div className="d-flex flex-row-fluid">
        <div className="md-row-12">
          <div className="d-flex flex-column flex-row-fluid">
              <div className="d-flex flex-column-fluid">
                  {/* <span className="text-white">Fixed Height</span> */}
                  <div
                    id='kt_toolbar_container'
                    className={clsx(classes.toolbarContainer.join(' '), 'd-flex flex-stack')}
                  >
                    <div className="col-xl-9">
                      <div
                        // className='menu menu-lg-rounded menu-column menu-lg-row menu-state-bg menu-title-gray-700 menu-state-title-primary menu-state-icon-primary menu-state-bullet-primary menu-arrow-gray-400 fw-bold my-5 my-lg-0 align-items-stretch'
                        id='#kt_header_menu'
                        data-kt-menu='true'
                      >
                        <ToolbarMenu />
                      </div>
                    </div>
                    <div className="col-xl-3 float-right">
                      <div className='d-flex align-items-center py-1'>
                        <div className='d-flex align-items-center position-relative me-4'> 
                          <div className="d-flex align-items-stretch flex-shrink-0" id="selection_menu_1"> 
                            <select className="form-select" aria-label="Select example">
                              <option>gespeicherter Suchprofile</option>
                              <option value="1">Genehmigungen ERNST</option>
                              <option value="2">Dokumente Bernauer Strasse</option>
                            </select>
                          </div>
                          
                          <div className='d-flex align-items-center position-relative me-4'>
                            <div className="d-flex flex-row-fluid flex-center align-items-center position-relative me-4">
                                <KTSVG
                                  path="/media/icons/duotune/general/gen035.svg"
                                  className="cursor-pointer svg-icon bg-gray svg-icon-5x svg-icon-gray-900"
                                  data-kt-menu-trigger="click"
                                  // data-kt-menu-attach="parent"
                                  // data-kt-menu-placement="bottom-end"
                                  // data-kt-menu-flip="bottom"
                                />
                            </div>
                          </div> 
                        </div>   
                      </div>
                    </div>
                  </div>
              </div>

              <div className="d-flex flex-column-fluid flex-center">
                  {/* <span className="text-white">Fluid Height</span> */}
                  <div
                    className={clsx(classes.toolbarContainer.join(' '), 'd-flex flex-stack')}
                    id='kt_toolbar_container2'
                  >
                      <Toolbar2 />
                  </div>
              </div>

              <div className="d-flex flex-column-fluid flex-center">
                  {/* <span className="text-white">Fluid Height</span> */}
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
           
      {/* <div
        id='kt_toolbar_container'
        className={clsx(classes.toolbarContainer.join(' '), 'd-flex flex-stack')}
      >
        <div
          // className='menu menu-lg-rounded menu-column menu-lg-row menu-state-bg menu-title-gray-700 menu-state-title-primary menu-state-icon-primary menu-state-bullet-primary menu-arrow-gray-400 fw-bold my-5 my-lg-0 align-items-stretch'
          id='#kt_header_menu'
          data-kt-menu='true'
        >
          <ToolbarMenu />
        </div>

        <div className='d-flex align-items-center py-1' >
          <div className='d-flex align-items-center position-relative me-4'> 
            <div className="d-flex align-items-stretch flex-shrink-0" id="selection_menu_1"> 
              <select className="form-select" aria-label="Select example">
                <option>gespeicherter Suchprofile</option>
                <option value="1">Genehmigungen ERNST</option>
                <option value="2">Dokumente Bernauer Strasse</option>
              </select>
            </div>
            
            <div className='d-flex align-items-center position-relative me-4'>
            
              <div className="d-flex flex-row-fluid flex-center align-items-center position-relative me-4">
                  <KTSVG
                    path="/media/icons/duotune/general/gen035.svg"
                    className="cursor-pointer svg-icon bg-gray svg-icon-5x svg-icon-gray-900"
                    data-kt-menu-trigger="click"
                    // data-kt-menu-attach="parent"
                    // data-kt-menu-placement="bottom-end"
                    // data-kt-menu-flip="bottom"
                  />
              </div>
            </div> 
          </div>   
        </div>
      </div>

      <div
        className={clsx(classes.toolbarContainer.join(' '), 'd-flex flex-stack')}
        id='kt_toolbar_container2'
      >
          <Toolbar2 />
      </div> */}
    </div>
  )
}

export {Toolbar1}
