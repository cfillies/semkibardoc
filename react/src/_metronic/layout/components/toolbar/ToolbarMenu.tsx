import React, { Key, useState } from 'react'
import {MenuItem} from '../header/MenuItem'
import {MenuInnerWithSub} from '../header/MenuInnerWithSub'
import {MegaMenu} from '../header/MegaMenu'
import {useIntl} from 'react-intl'
import { TypeOf } from 'yup'
import { right } from '@popperjs/core'

import { useDispatch, useSelector } from 'react-redux'
import { fetchDocumentsAsync, docList, fetchStatus } from '../../../../features/filter/documentsSlice'
import { DocumentsInterface, FilterInterface } from '../../../../utils/interfaces'
import { setNewFilter, newFilter, changeState, updateChangeType } from '../../../../features/filter/filterObjectSlice'
import { reset } from '../../../../features/filter/counterSlice'

const primary = "btn btn-bg-light border border-gray-200 btn-color-primary"
const muted = "btn btn-bg-light border border-gray-200 btn-color-muted"

const filterArray = [
  {filter: 'Antrag'},
  {filter: 'Eigangsbestätigung'},
  {filter: 'Genehmigung'},
  {filter: 'Versagung'},
  {filter: 'Stellungnahme'},
  {filter: 'Anhorungrag'}
]

let booleanFilterArray = 
  {"Antrag": true,
  "Eigangsbestätigung": true,
  "Genehmigung": true,
  "Versagung": true,
  "Stellungnahme": true,
  "Anhorungrag": true}

let requestFilterArray: FilterInterface = 
  {
    "Antrag": true,
    "Eigangsbestätigung": true,
    "Genehmigung": true,
    "Versagung": true,
    "Stellungnahme": true,
    "Anhorungrag": true,
    "from": 0,
    "size": 10
  }


export function ToolbarMenu() {
  
  const dispatch = useDispatch()
  const updatedFilter: FilterInterface = useSelector(newFilter);

  const [buttonColor, setButtonColor] = useState([primary, primary, primary, primary, primary, primary]);

  const toggleButtonHandler = (index: number) => {
    const newColor = buttonColor[index] === primary ? muted : primary;
    let newColorArray = [...buttonColor]
    newColorArray[index] = newColor
    setButtonColor(newColorArray)

    let typedFilter = filterArray[index].filter as keyof typeof booleanFilterArray
    const toggledFilter = typedFilter!
    const result = !booleanFilterArray[toggledFilter]
    booleanFilterArray[toggledFilter] = result
   
   
    requestFilterArray[toggledFilter] = result
    dispatch(setNewFilter({updateFilterObject: requestFilterArray}))
    dispatch(reset())
    dispatch(changeState())
    dispatch(updateChangeType({newChange: 'filtering'}))
 
  }

  return (
    <>
      {
        filterArray.map(
            (item, index) => {
              return (
                <a 
                  href="#" 
                  className={buttonColor[index]} 
                  key={index}
                  onClick={() => toggleButtonHandler(index)}
                  style={{marginRight:"10px"}}
                >
                  {item.filter}
                </a>
              )
            }
          )
      }
    </>
  )
}
