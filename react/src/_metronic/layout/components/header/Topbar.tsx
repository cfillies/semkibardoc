import clsx from 'clsx'
import React, {FC} from 'react'
import {KTSVG, toAbsoluteUrl} from '../../../helpers'
import {HeaderNotificationsMenu, HeaderUserMenu, QuickLinks, Search} from '../../../partials'
import {useLayout} from '../../core'

const toolbarButtonMarginClass = 'ms-1 ms-lg-3',
  toolbarButtonHeightClass = 'w-30px h-30px w-md-40px h-md-40px',
  toolbarUserAvatarHeightClass = 'symbol-30px symbol-md-40px',
  toolbarButtonIconSizeClass = 'svg-icon-1'

const Topbar: FC = () => {
  const {config} = useLayout()

  return (
    <div className='d-flex align-items-stretch flex-shrink-0'>
      {/* Search */}
      {/* <div className={clsx('d-flex align-items-stretch', toolbarButtonMarginClass)}>
        <Search />
      </div> */}
      <div className='d-flex align-items-center position-relative me-4'>
          {/* Favorites Button */}
          <a
            href='#'
            className='btn btn-sm btn-light btn-color-muted btn-active-light-danger px-4 py-2'
          >
            <KTSVG path='/media/icons/duotune/general/gen030.svg' className='svg-icon-2' />
            Merkzettel 29
          </a>
        </div>
    </div>
  )
}

export {Topbar}
