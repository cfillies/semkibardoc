/* eslint-disable react/jsx-no-target-blank */
import React, { useState } from 'react'
import {AsideMenuItemWithSub} from './AsideMenuItemWithSub'
import { useDispatch, useSelector } from 'react-redux'
import { changeState, updateChangeType, setAsideItemConfiguration, asideFiltersConfigurations, changeLoadingFiltersState, setSearchState, changeLoadingHorizontalFiltersState, currentFilterCounter, updateFilterCounter } from '../../../../features/filter/filterObjectSlice'
import { InnerAsideMenuInterface, AsideFiltersInterface, AsideFiltersCounterInterface } from '../../../../utils/interfaces'
import { reset } from '../../../../features/filter/counterSlice'

type Props = {
  fieldName: string,
  document: InnerAsideMenuInterface,
  idx: number
}

const ShowAsideItemHandler: React.FC<Props> = ({document, fieldName, idx}) => {
    // const [docTypFilters, setDocTypFilters] = useState<InnerAsideMenuInterface[]>([] as InnerAsideMenuInterface[]);
  const asideItemConf = useSelector(asideFiltersConfigurations)
  const filtersCounter = useSelector(currentFilterCounter)
  let newFiltersCounter = {...filtersCounter}
  // const muted = 'btn btn-sm btn-white btn-color-muted px-4 py-2'
  // const lightDanger = 'btn btn-sm btn-light btn-light-primary px-4 py-2'
  const currentFieldName = fieldName as keyof typeof asideItemConf
  
  const filterIndex = asideItemConf[currentFieldName].indexOf(document.value, 0);
  const filterFlag = filterIndex != -1

  // const muted = 'btn btn-sm btn-white btn-color-muted px-4 py-2'
  const muted = "btn btn-bg-light btn-color-gray-900"
  const lightDanger = 'btn btn-sm btn-light btn-light-primary px-4 py-2'

  const [buttonMerken, setButtonMerken] = useState(false)
  const [buttonColor, setButtonColor] = useState(muted)

  const filterName = fieldName === 'path'? document.value.split("\\")[document.value.split("\\").length - 1]: document.value

  const toggleButtonHandler = () => {
    // console.log("toggleButtonHandler")
    if (buttonMerken){
      // console.log("if")
      setButtonMerken(false)
      setButtonColor(muted)
    }
    else {
      // console.log("else")
      setButtonMerken(true)
      setButtonColor(lightDanger)
    }
  }

  const dispatch = useDispatch()

  return (
        <a 
          href="#"
          ref={React.createRef()}
          // className={filterFlag? lightDanger: muted}
          onClick={() => {
            dispatch(changeState())
            dispatch(changeLoadingFiltersState())
            let asideFilters = {} as typeof asideItemConf;
            let key: keyof AsideFiltersInterface;
            for (key in asideItemConf) {
              asideFilters[key] = [...asideItemConf[key]]
            }
            const fieldList = fieldName as keyof typeof asideItemConf;
            const value = document.value
            const index = asideFilters[fieldList].indexOf(value, 0);
            if (index > -1) {
              asideFilters[fieldList].splice(index, 1);
            }
            else {
              asideFilters[fieldList].push(value)
            }
            dispatch(reset())
            dispatch(changeLoadingHorizontalFiltersState())
            dispatch(setAsideItemConfiguration({updateAsideItemConfig:asideFilters}))
            dispatch(updateChangeType({newChange: 'asideItem'}))
            // dispatch(updateChangeType({newChange: 'horizontalItem'}))
            dispatch(setSearchState({searchingState:false}))

            const filterCounterKey = fieldName as keyof AsideFiltersCounterInterface
            newFiltersCounter[filterCounterKey] = 1
            dispatch(updateFilterCounter({filterCounter: newFiltersCounter}))

            toggleButtonHandler();
            }
          }
        >
          <AsideMenuItemWithSub
            to='/crafted/pages'
            title={filterName.concat(' (' + document.count.toString() + ')')}
            // fontIcon='bi-archive'
            flag={filterFlag}
          >
            
          </AsideMenuItemWithSub>
      </a> 
  )
}
    
  

export {ShowAsideItemHandler}
