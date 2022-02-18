import {FC} from 'react'
import {KTSVG} from '../../../helpers'

const Topbar: FC = () => {

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
