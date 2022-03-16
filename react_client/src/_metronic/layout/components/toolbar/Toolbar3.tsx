import React, {FC} from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { reset } from '../../../../features/filter/counterSlice'
import { changeState, updateChangeType, setAsideItemConfiguration, asideFiltersConfigurations, changeLoadingFiltersState, setSearchState, changeLoadingHorizontalFiltersState } from '../../../../features/filter/filterObjectSlice'
import { AsideFiltersInterface } from '../../../../utils/interfaces'


const Toolbar3: FC = () => {
  const asideItemConf = useSelector(asideFiltersConfigurations)
  let asideItemList = [] as String[]
  let key: keyof AsideFiltersInterface;
  const dispatch = useDispatch()
  for(key in asideItemConf) {
    let currentDoc = asideItemConf[key]
    asideItemList = asideItemList.concat(currentDoc)
  }
  // console.log(asideItemConf)


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
                className="btn btn-bg-light border border-gray-200 btn-color-muted"
                style={{marginRight:"10px"}}
                key={index}
                onClick={() => {
                    toggleButtonHandler(doc);
                  }
                } 
                >
                
                {doc}
              </a>
            )
          )
        }
      </ul>
    </>
  )
}

export {Toolbar3}
