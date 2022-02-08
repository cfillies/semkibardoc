import React, {FC, FormEvent, useRef} from 'react'
import clsx from 'clsx'
import {useLayout} from '../../core'
import {KTSVG} from '../../../helpers'

import { useSelector, useDispatch } from 'react-redux'
import { increment, decrement, selectCount, } from '../../../../features/filter/counterSlice'
import { setNewFilter, changeState, newFilter, updateChangeType, setSearchConfiguration } from '../../../../features/filter/filterObjectSlice'
import { FilterInterface } from '../../../../utils/interfaces'
import { totalPages } from '../../../../features/filter/totalPagesSlice'


const Toolbar2: FC = () => {
  const {classes} = useLayout()

  const count: number = useSelector(selectCount);
  const updatedFilter: FilterInterface = useSelector(newFilter);
  const currentTotalPages =  useSelector(totalPages);
  const dispatch = useDispatch();

  let requestFilterArray = {...updatedFilter}
 
  const searchInputRef = useRef<HTMLInputElement>(null);
  const selectionInputRef = useRef<HTMLSelectElement>(null);

  function submitHandler(event: FormEvent<HTMLFormElement>) {
    console.log("submitHandler");
    event.preventDefault();
    

    if (null !== searchInputRef.current && null !== selectionInputRef.current) {
      const enteredSearch = searchInputRef.current.value; 
      const selectionSearch = selectionInputRef.current.value;
      const searchData = {
        search: enteredSearch,
        field: selectionSearch
      }
      console.log(searchData)
      dispatch(setSearchConfiguration({updateSearchConfig:searchData}))
      dispatch(updateChangeType({newChange:'searching'}))
      dispatch(changeState())
    }
  }

  return (
    <div className='toolbar' id='kt_toolbar2' style={{marginTop:"55px", position:"fixed"}}>
      {/* begin::Container */}
      <div
        id='kt_toolbar_container2'
        className={clsx(classes.toolbarContainer.join(' '), 'd-flex flex-stack')}
      >
        {/* begin::Actions */}
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

        <form className='form' onSubmit={(e) => submitHandler(e)}>
          <div className='d-flex flex-grow-1 align-items-left py-1'>
            <div className='d-flex align-items-center position-relative me-4'>
              <KTSVG
                  path='/media/icons/duotune/general/gen021.svg'
                  className='svg-icon-3 position-absolute ms-3'
                />

              {/* Search bar */}
              <input
                type='text'
                id='kt_filter_search'
                className='form-control form-control-white form-control-mg ps-9'
                placeholder='Search'
                ref={searchInputRef}
              />
            </div>
          </div>
        </form>

        <div className='d-flex align-items-center py-1' >

          <div className='d-flex flex-row-fluid align-items-center position-relative me-4'> 
            <div className="d-flex card flex-center align-items-center position-relative me-4"> 
              <span><h4> Seite</h4></span>
            </div> 
            <div className="d-flex card flex-center align-items-center position-relative me-4"> 
              <span><h4> {count}</h4></span>
            </div> 
            <div className="d-flex card flex-center align-items-center position-relative me-4"> 
              <span><h4> von</h4></span>
            </div> 
            <div className="d-flex card flex-center align-items-center position-relative me-4"> 
              <span><h4>{currentTotalPages}</h4></span>
            </div> 

            <div className='d-flex flex-column-fluid align-items-center position-relative me-4' id="back_button"> 
              <a href="#" className="btn btn-active-icon-dark btn-active-text-dark"
                onClick={() => 
                  {
                    if (count>1) {
                      dispatch(decrement())
                      if (count === 1){
                        requestFilterArray.from = count * requestFilterArray.size
                      }
                      else {
                        requestFilterArray.from = (count - 2) * requestFilterArray.size
                      }
                      dispatch(setNewFilter({updateFilterObject: requestFilterArray}))
                      dispatch(changeState())
                      dispatch(updateChangeType({newChange: 'newPage'}))
                    }
                  }
                }
              >
                <span className="svg-icon svg-icon-1">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect opacity="0.5" x="6" y="11" width="13" height="2" rx="1" fill="black"/>
                    <path d="M8.56569 11.4343L12.75 7.25C13.1642 6.83579 13.1642 6.16421 12.75 5.75C12.3358 5.33579 11.6642 5.33579 11.25 5.75L5.70711 11.2929C5.31658 11.6834 5.31658 12.3166 5.70711 12.7071L11.25 18.25C11.6642 18.6642 12.3358 18.6642 12.75 18.25C13.1642 17.8358 13.1642 17.1642 12.75 16.75L8.56569 12.5657C8.25327 12.2533 8.25327 11.7467 8.56569 11.4343Z" fill="black"/>
                  </svg>
                </span>
              </a>
            </div> 

            <div className='d-flex flex-column-fluid align-items-center position-relative me-4' id="forward_button">
              <a href="#" className="btn btn-active-icon-dark btn-active-text-dark" 
                onClick={() => 
                  {
                    if (count<currentTotalPages) {
                      dispatch(increment())
                      requestFilterArray.from = count * requestFilterArray.size
                      dispatch(setNewFilter({updateFilterObject: requestFilterArray}))
                      dispatch(changeState())
                      dispatch(updateChangeType({newChange: 'newPage'}))
                    }
                  }
                }
              >
                <span className="svg-icon svg-icon-1">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect opacity="0.5" x="18" y="13" width="13" height="2" rx="1" transform="rotate(-180 18 13)" fill="black"/>
                    <path d="M15.4343 12.5657L11.25 16.75C10.8358 17.1642 10.8358 17.8358 11.25 18.25C11.6642 18.6642 12.3358 18.6642 12.75 18.25L18.2929 12.7071C18.6834 12.3166 18.6834 11.6834 18.2929 11.2929L12.75 5.75C12.3358 5.33579 11.6642 5.33579 11.25 5.75C10.8358 6.16421 10.8358 6.83579 11.25 7.25L15.4343 11.4343C15.7467 11.7467 15.7467 12.2533 15.4343 12.5657Z" fill="black"/>
                  </svg>
                </span>
              </a>
            </div> 

          </div>
        </div>
         {/* end::Actions */}
      </div>
      {/* end::Container */}
    </div>
  )
}

export {Toolbar2}
