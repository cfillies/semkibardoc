import {FC} from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { increment, decrement, selectCount, reset, } from '../../../../features/filter/counterSlice'
import { changeState, updateChangeType, setAsideItemConfiguration, asideFiltersConfigurations, changeLoadingFiltersState, setSearchState, changeLoadingHorizontalFiltersState } from '../../../../features/filter/filterObjectSlice'
import { AsideFiltersInterface } from '../../../../utils/interfaces'
import { totalPages } from '../../../../features/filter/totalPagesSlice'


const Toolbar3: FC = () => {
  const count: number = useSelector(selectCount);
  const currentTotalPages =  useSelector(totalPages);

  const asideItemConf = useSelector(asideFiltersConfigurations)
  let asideItemList = [] as String[]
  let key: keyof AsideFiltersInterface;
  const dispatch = useDispatch()
  for(key in asideItemConf) {
    let currentDoc = asideItemConf[key]
    asideItemList = asideItemList.concat(currentDoc)
  }

  const toggleButtonHandler = (doc: String) => {

    let asideFilters = {} as typeof asideItemConf;
    for (key in asideItemConf) {
      asideFilters[key] = [...asideItemConf[key]]
    }

    for(key in asideFilters) {
      const index = asideFilters[key].indexOf(doc, 0);
      if (index > -1) {
        asideFilters[key].splice(index, 1);
      }
    }

    dispatch(changeState())
    dispatch(changeLoadingFiltersState())

    dispatch(reset())
    dispatch(changeLoadingHorizontalFiltersState())
    dispatch(setAsideItemConfiguration({updateAsideItemConfig:asideFilters}))
    dispatch(updateChangeType({newChange: 'asideItem'}))
    dispatch(updateChangeType({newChange: 'horizontalItem'}))
    dispatch(setSearchState({searchingState:false}))
  }

  
  return (
    <>
      <ul>
        {
          asideItemList?.map(
            (doc, index) => (
              <a 
                href="#" 
                className="btn btn-bg-light border border-gray-200 btn-color-gray-900"
                // className="btn btn-flush border border-gray-900"
                style={{marginRight:"10px", marginBottom:"4px"}}
                key={index}
                onClick={() => {
                    toggleButtonHandler(doc);
                  }
                } 
                >
                  {doc}
                  <span className="svg-icon svg-icon-1">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect opacity="0.3" x="2" y="2" width="20" height="20" rx="10" fill="black"/>
                      <rect x="7" y="15.3137" width="12" height="2" rx="1" transform="rotate(-45 7 15.3137)" fill="black"/>
                      <rect x="8.41422" y="7" width="12" height="2" rx="1" transform="rotate(45 8.41422 7)" fill="black"/>
                    </svg>
                  </span>
              </a>
            )
          )
        }
      </ul>
    
      {
      currentTotalPages > 0 && 
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
      }
    </>
  )
}

export {Toolbar3}
