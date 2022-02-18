import { useEffect, useState } from 'react'

import { useDispatch, useSelector } from 'react-redux'
import { asideFiltersConfigurations, setAsideItemConfiguration, setSearchState } from '../../../../features/filter/filterObjectSlice'
import { AsideFiltersInterface, InnerAsideMenuInterface } from '../../../../utils/interfaces'
import { changeState, updateChangeType } from '../../../../features/filter/filterObjectSlice'
import { reset } from '../../../../features/filter/counterSlice'

const primary = "btn btn-bg-light border border-gray-200 btn-color-primary"
const muted = "btn btn-bg-light border border-gray-200 btn-color-muted"

export function ToolbarMenu() {
  
  const dispatch = useDispatch()
  const asideItemConf = useSelector(asideFiltersConfigurations);

  const [isLoading, setIsLoading] = useState(true);
  const [currentHorizontalFilters, setCurrentHorizontalFilters] = useState<InnerAsideMenuInterface[]>([] as InnerAsideMenuInterface[]);
  const [buttonColor, setButtonColor] = useState([] as String[]);

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
    const value = currentHorizontalFilters[index].value
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
    dispatch(updateChangeType({newChange: 'asideItem'}))
    dispatch(setSearchState({searchingState:false}))
 
  }


  useEffect(() => {
    setIsLoading(true);
    
    fetch(
      // 'http://localhost:5000/aside/'
      'http://localhost:5000/search/resolved2_facets'
    )
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setIsLoading(false);
        setCurrentHorizontalFilters(data.doctype);
        
        let buttonColorTemp = Array.apply(null, Array(data.doctype.length)).map(String.prototype.valueOf, muted);
        setButtonColor(buttonColorTemp)
      });
      
  }, []);

  if (isLoading) {
    return (
      <section>
        <p>Loading...</p>
      </section>
    );
  }

  return (
    <>
      {
        currentHorizontalFilters
        // .slice(0,6)
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
