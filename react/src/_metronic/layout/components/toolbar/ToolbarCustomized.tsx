/* eslint-disable jsx-a11y/anchor-is-valid */
import clsx from 'clsx'
import React, {FC} from 'react'
import {KTSVG} from '../../../helpers'
import {useLayout} from '../../core'
import {ToolbarMenu} from './ToolbarMenu'

const ToolbarCustomized : FC = () => {
  const {classes} = useLayout()

  return (
    // <div style={{position:'fixed'}}>
    <div className="d-flex flex-column flex-row-fluid">
      <div id="kt_toolbar_container1" 
           className="card container-fluid d-flex flex-stack border border-gray-400"
           style={{marginTop:"35px"}}
      >
        <div className="d-flex flex-row flex-column-fluid h-75px">
            
            <div className="d-flex flex-row-auto w-1000px flex-center border border-gray-400">
              <ToolbarMenu />
            </div>

            <div className="d-flex flex-row-fluid flex-center">
              <div className='accordion' id='kt_accordion_1'>
                <div className='accordion-item'>
                  <h2 className='accordion-header' id='kt_accordion_1_header_1'>
                    <button
                      className='accordion-button fs-4 fw-bold collapsed'
                      type='button'
                      data-bs-toggle='collapse'
                      data-bs-target='#kt_accordion_1_body_1'
                      aria-expanded='false'
                      aria-controls='kt_accordion_1_body_1'
                    >
                      Accordion Item #1
                    </button>
                  </h2>
                  <div
                    id='kt_accordion_1_body_1'
                    className='accordion-collapse collapse'
                    aria-labelledby='kt_accordion_1_header_1'
                    data-bs-parent='#kt_accordion_1'
                  >
                    <div className='accordion-body'>
                      <strong>This is the first item's accordion body.</strong>It is hidden by
                      default, until the collapse plugin adds the appropriate classes that we use to
                      style each element. These classes control the overall appearance, as well as the
                      showing and hiding via CSS transitions. You can modify any of this with custom
                      CSS or overriding our default variables. It's also worth noting that just about
                      any HTML can go within the
                      <code>.accordion-body</code>, though the transition does limit overflow.
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="d-flex flex-row-fluid flex-center align-items-center position-relative me-4 border border-gray-400">
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

      <div id="kt_toolbar_container2" className="card container-fluid d-flex flex-stack border border-gray-400">
        <div className="d-flex flex-row flex-column-fluid h-75px">
          <div className="d-flex flex-row-auto w-1000px flex-center border border-gray-400">

            <div className="d-flex flex-row-fluid flex-center border border-gray-400">
              <div className='accordion' id='kt_accordion_1'>
                <div className='accordion-item'>
                  <h2 className='accordion-header' id='kt_accordion_1_header_1'>
                    <button
                      className='accordion-button fs-4 fw-bold collapsed'
                      type='button'
                      data-bs-toggle='collapse'
                      data-bs-target='#kt_accordion_1_body_1'
                      aria-expanded='false'
                      aria-controls='kt_accordion_1_body_1'
                    >
                      Accordion Item #1
                    </button>
                  </h2>
                  <div
                    id='kt_accordion_1_body_1'
                    className='accordion-collapse collapse'
                    aria-labelledby='kt_accordion_1_header_1'
                    data-bs-parent='#kt_accordion_1'
                  >
                    <div className='accordion-body'>
                      <strong>This is the first item's accordion body.</strong>It is hidden by
                      default, until the collapse plugin adds the appropriate classes that we use to
                      style each element. These classes control the overall appearance, as well as the
                      showing and hiding via CSS transitions. You can modify any of this with custom
                      CSS or overriding our default variables. It's also worth noting that just about
                      any HTML can go within the
                      <code>.accordion-body</code>, though the transition does limit overflow.
                    </div>
                  </div>
                </div>
              </div> 

            </div>

            <div className="d-flex flex-row-fluid flex-center border border-gray-400">
              <div className='d-flex align-items-center position-relative me-4'>
                <KTSVG
                  path='/media/icons/duotune/general/gen021.svg'
                  className='svg-icon-3 position-absolute ms-3'
                />

                {/* Search bar */}
                <input
                  type='text'
                  id='kt_filter_search'
                  className='form-control form-control-white form-control-sm w-auto ps-9'
                  placeholder='Search'
                />
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  )
}

export {ToolbarCustomized}

