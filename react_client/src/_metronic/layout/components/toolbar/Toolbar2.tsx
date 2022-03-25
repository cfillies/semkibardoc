import {FC, FormEvent, useRef} from 'react'
import clsx from 'clsx'
import {useLayout} from '../../core'
import {KTSVG} from '../../../helpers'

import { useSelector, useDispatch } from 'react-redux'
import { increment, decrement, selectCount, reset, } from '../../../../features/filter/counterSlice'
import { changeState, updateChangeType, setSearchConfiguration, setSearchState, changeLoadingHorizontalFiltersState, changeLoadingFiltersState } from '../../../../features/filter/filterObjectSlice'


const Toolbar2: FC = () => {
  const {classes} = useLayout()

  
  const dispatch = useDispatch();
 
  const searchInputRef = useRef<HTMLInputElement>(null);
  const selectionInputRef = useRef<HTMLSelectElement>(null);

  function submitHandler(event: FormEvent<HTMLFormElement>) {
    // console.log("submitHandler");
    event.preventDefault();
    

    if (null !== searchInputRef.current && null !== selectionInputRef.current) {
      const enteredSearch = searchInputRef.current.value; 
      const selectionSearch = selectionInputRef.current.value;
      const searchData = {
        search: enteredSearch,
        field: selectionSearch
      }
      // console.log(searchData)
      dispatch(reset())
      dispatch(setSearchConfiguration({updateSearchConfig:searchData}))
      dispatch(updateChangeType({newChange:'searching'}))
      dispatch(changeState())
      dispatch(setSearchState({searchingState:true}))

      dispatch(changeLoadingHorizontalFiltersState())
      dispatch(changeLoadingFiltersState())
      // dispatch(updateChangeType({newChange: 'asideItem'}))
      // dispatch(updateChangeType({newChange: 'horizontalItem'}))
    }
  }

  return (
    <div id='kt_toolbar2' style={{width:"100%"}}>
      {/* begin::Container */}
      <div
        id='kt_toolbar_container2'
        className={clsx(classes.toolbarContainer.join(' '), 'd-flex flex-stack')}
      >
        <div className="d-flex align-items-stretch justify-content-between flex-lg-grow-1">
          <div className="col-xl-1" style={{marginTop:"4px"}}>
            <div className='d-flex align-items-center py-1'>
              <div className='me-4' id="selection_menu_2"> 
                <select className="form-select" aria-label="Select example" ref={selectionInputRef}>
                  <option>Überall</option>
                  <option value="1">Fulltext</option>
                  <option value="2">Addresse</option>
                  <option value="3">ObjNr</option>
                  <option value="3">Hida Text</option>
                </select>
              </div>
            </div>
          </div>
          <div className="col-xl-8" style={{marginTop:"4px"}}>
            <form className='form' onSubmit={(e) => submitHandler(e)} style={{width:"100%"}}>
              <div className='d-flex flex-grow-1 align-items-left py-1' style={{width:"100%"}}>
                <div className='d-flex align-items-center position-relative me-4' style={{width:"100%"}}>
                  <KTSVG
                      path='/media/icons/duotune/general/gen021.svg'
                      className='svg-icon-3 position-absolute ms-3'
                    />

                  <input
                    type='text'
                    id='kt_filter_search'
                    className='form-control form-control-white form-control-mg ps-9'
                    placeholder='Suche'
                    ref={searchInputRef}
                  />
                </div>
              </div>
            </form>
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
      {/* end::Container */}
    </div>
  )
}

export {Toolbar2}
