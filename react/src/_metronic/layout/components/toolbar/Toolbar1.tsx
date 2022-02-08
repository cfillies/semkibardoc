/* eslint-disable jsx-a11y/anchor-is-valid */
import clsx from 'clsx'
import React, {FC} from 'react'
import {KTSVG} from '../../../helpers'
import {useLayout} from '../../core'
import {DefaultTitle} from '../header/page-title/DefaultTitle'
import {ToolbarMenu} from './ToolbarMenu'

const Toolbar1: FC = () => {
  const {classes} = useLayout()

  return (
    <div className='toolbar' id='kt_toolbar'>
      {/* begin::Container */}
      <div
        id='kt_toolbar_container'
        className={clsx(classes.toolbarContainer.join(' '), 'd-flex flex-stack')}
      >
        {/* <DefaultTitle /> */}
        <div
          className='menu menu-lg-rounded menu-column menu-lg-row menu-state-bg menu-title-gray-700 menu-state-title-primary menu-state-icon-primary menu-state-bullet-primary menu-arrow-gray-400 fw-bold my-5 my-lg-0 align-items-stretch'
          id='#kt_header_menu'
          data-kt-menu='true'
        >
          <ToolbarMenu />

        </div>

        {/* begin::Actions */}
        <div className='d-flex align-items-center py-1' style={{marginRight:"60px"}}>

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
          
          {/* begin::Wrapper */}
          {/* <div className='me-4'> */}
            {/* begin::Menu */}
            {/* <a
              href='#'
              className='btn btn-sm btn-flex btn-light btn-active-primary fw-bolder'
              data-kt-menu-trigger='click'
              data-kt-menu-placement='bottom-end'
              data-kt-menu-flip='top-end'
            >
              <KTSVG
                path='/media/icons/duotune/general/gen031.svg'
                className='svg-icon-5 svg-icon-gray-500 me-1'
              />
              Filter
            </a> */}

            {/* end::Menu */}
          {/* </div> */}
          {/* end::Wrapper */}

          {/* begin::Button */}

          {/* <a
            href='#'
            className='btn btn-sm btn-primary'
            data-bs-toggle='modal'
            data-bs-target='#kt_modal_create_app'
            id='kt_toolbar_primary_button'
          >
            Create
          </a> */}
          {/* end::Button */}
        </div>
        {/* end::Actions */}
      </div>
      {/* end::Container */}
    </div>
  )
}

export {Toolbar1}
