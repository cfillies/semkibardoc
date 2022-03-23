import { useState } from 'react'

import { useDispatch, useSelector } from 'react-redux'
import { asideFiltersConfigurations, setAsideItemConfiguration, setSearchState, currentChangeType, changeLoadingHorizontalFiltersState, currentDocTypFilters, changeLoadingFiltersState, searchConfigurations } from '../../../../features/filter/filterObjectSlice'
import { AsideFiltersInterface, InnerAsideMenuInterface } from '../../../../utils/interfaces'
import { changeState, updateChangeType } from '../../../../features/filter/filterObjectSlice'
import { reset } from '../../../../features/filter/counterSlice'
import {fetchFilters} from '../../../../features/filter/documentsSlice'

const primary = "btn btn-bg-light border border-gray-200 btn-color-primary"
const muted = "btn btn-bg-light border border-gray-200 btn-color-muted"

export function ToolbarMenu() {
  
  const dispatch = useDispatch()
  const asideItemConf = useSelector(asideFiltersConfigurations);
  // const docTyp = useSelector(docTypFilterList);
  // const docTypStatus = useSelector(docTypFilterStatus);
  const currentFiltersChangeStatus = useSelector(currentDocTypFilters)
  const changeType = useSelector(currentChangeType)
  const searchConf = useSelector(searchConfigurations)
  const [isLoading, setIsLoading] = useState(true);
  // const [currentHorizontalFilters, setCurrentHorizontalFilters] = useState<InnerAsideMenuInterface[]>([] as InnerAsideMenuInterface[]);
  const [docTypFilters, setDocTypFilters] = useState<InnerAsideMenuInterface[]>([] as InnerAsideMenuInterface[]);
  const [buttonColor, setButtonColor] = useState([] as String[]);

  const updateFiltersHandler = async () => {

    if (changeType === 'searching' || changeType === 'asideItem' || changeType === 'filtering' || changeType === 'horizontalItem' ) {
      // console.log('Searching')
      try {
        const t = await dispatch(fetchFilters({filterQuery: asideItemConf, searchQuery: searchConf}));

        let jsonResult = JSON.stringify(t);
        let objResult = JSON.parse(jsonResult);
        setDocTypFilters(objResult.payload.doctype)
        setIsLoading(false);
      } 
      catch (err) {
        console.error('Failed to save the post: ', err)
      } 
    }

    // else if (changeType === 'searching') {
    //   console.log('Searching')
    //   try {
    //     const t = await dispatch(searchFiltersAsync(searchConf));

    //     let jsonResult = JSON.stringify(t);
    //     let objResult = JSON.parse(jsonResult);
    //     setDocTypFilters(objResult.payload.doctype)
    //     setIsLoading(false);
    //   } 
    //   catch (err) {
    //     console.error('Failed to save the post: ', err)
    //   } 
    // }
  }

  const toggleButtonHandler = (index: number) => {
    const newColor = buttonColor[index] === primary ? muted : primary;
    buttonColor[index] = newColor
    
    // let typedFilter = filterArray[index].filter as keyof typeof booleanFilterArray
    // const toggledFilter = typedFilter!
    // const result = !booleanFilterArray[toggledFilter]
    // booleanFilterArray[toggledFilter] = result
   
   
    // requestFilterArray[toggledFilter] = result
    // dispatch(setNewFilter({updateFilterObject: requestFilterArray}))
    
    let asideFilters = {} as typeof asideItemConf;
    let key: keyof AsideFiltersInterface;
    for (key in asideItemConf) {
      asideFilters[key] = [...asideItemConf[key]]
    }
    const fieldList = 'doctype' as keyof typeof asideItemConf;
    const value = docTypFilters[index].value
    const idx = asideFilters[fieldList].indexOf(value, 0);
    if (idx > -1) {
      asideFilters[fieldList].splice(idx, 1);
    }
    else {
      asideFilters[fieldList].push(value)
    }
    dispatch(setAsideItemConfiguration({updateAsideItemConfig:asideFilters}))

    dispatch(reset())
    dispatch(changeState())
    dispatch(setAsideItemConfiguration({updateAsideItemConfig:asideFilters}))
    dispatch(changeLoadingFiltersState())
    dispatch(updateChangeType({newChange: 'asideItem'}))
    dispatch(updateChangeType({newChange: 'horizontalItem'}))
    dispatch(setSearchState({searchingState:false}))
 
  }
  if (currentFiltersChangeStatus){
    const newData = updateFiltersHandler();
    dispatch(changeLoadingHorizontalFiltersState())
    // setIsLoading(false)
    // dispatch(setDocTypList({docTypFilterList:docTypFilters}))
  }

  if (docTypFilters.length > 0 && !currentFiltersChangeStatus && !isLoading) {
    let buttonColorTemp = Array.apply(null, Array(docTypFilters.length)).map(String.prototype.valueOf, muted);
    setButtonColor(buttonColorTemp)
    setIsLoading(true)
  }

  return (
    <>
      {
        docTypFilters
        
        .map(
            (item, index) => {
              return (
                <a 
                  href="#" 
                  className={buttonColor[index] as string} 
                  key={index}
                  onClick={() => toggleButtonHandler(index)}
                  style={{marginRight:"10px"}}
                >
                  {item.value.concat(' (' + item.count.toString() + ')')}
                </a>
              )
            }
          )
      }
    </>
  )
}
