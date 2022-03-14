/* eslint-disable react/jsx-no-target-blank */
import React, { useState } from 'react'
import AsideCheckBox from './AsideCheckBox'
import AsideCheckBox2 from './AsideCheckBox2'
import { AsideMenuInterface } from '../../../../utils/interfaces'
import { useDispatch, useSelector } from 'react-redux'
import { asideFiltersConfigurations, changeLoadingFiltersState, currentChangeType, currentLoadingFiltersState, searchConfigurations } from '../../../../features/filter/filterObjectSlice'
import { InnerAsideMenuInterface } from '../../../../utils/interfaces'
import { fetchFilters } from '../../../../features/filter/documentsSlice'
import {ShowAsideItemHandler} from './ShowAsideItemHandler'


type Props = {
  fieldName: string,
  document: InnerAsideMenuInterface,
  idx: number
}

type PropsDocs = {
  listFieldName: string,
  asideDocuments: InnerAsideMenuInterface[]
}

export function AsideMenuMain() {
  const [loadedDocuments, setLoadedDocuments] = useState<AsideMenuInterface>({} as AsideMenuInterface);
  // const [docTypFilters, setDocTypFilters] = useState<InnerAsideMenuInterface[]>([] as InnerAsideMenuInterface[]);
  const asideItemConf = useSelector(asideFiltersConfigurations)
  const changeType = useSelector(currentChangeType)
  const currentFiltersChangeStatus = useSelector(currentLoadingFiltersState)
  const searchConf = useSelector(searchConfigurations)
  // const docTyp = useSelector(docTypFilterList);
  
  // const [loadedDocumentsCounter, setLoadedDocumentsCounter] = useState<number>(0);
  // const [itemsNumberToShow, setItemsNumberToShow] = useState<number>(3);

  // const muted = 'btn btn-sm btn-white btn-color-muted px-4 py-2'
  // const lightDanger = 'btn btn-sm btn-light btn-light-primary px-4 py-2'

  // const [buttonMerken, setButtonMerken] = useState(false)
  // const [buttonColor, setButtonColor] = useState(muted)

  // const toggleButtonHandler = () => {
  //   if (buttonMerken){
  //     setButtonMerken(false)
  //     setButtonColor(muted)
  //   }
  //   else {
  //     setButtonMerken(true)
  //     setButtonColor(lightDanger)
  //   }
  // }

  const dispatch = useDispatch()

  const updateFiltersHandler = async () => {

    if (changeType === 'searching' || changeType === 'asideItem' || changeType === 'filtering' || changeType === 'horizontalItem') {
      if (changeType === 'searching') {
        console.log('searching')
      }
      
      try {
        const t = await dispatch(fetchFilters({filterQuery: asideItemConf, searchQuery: searchConf}));

        let jsonResult = JSON.stringify(t);
        let objResult = JSON.parse(jsonResult);
        setLoadedDocuments(objResult.payload);
        // setDocTypFilters(objResult.payload.doctype)
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
    //     setLoadedDocuments(objResult.payload);
    //     setIsLoading(false);
    //   } 
    //   catch (err) {
    //     console.error('Failed to save the post: ', err)
    //   } 
    // }
  }

  // const ShowAsideItemHandler: React.FC<Props> = ({document, fieldName, idx}) => { 

  //   return (
  //         <a 
  //           href="#"
  //           ref={React.createRef()}
  //           className={buttonColor}
  //           onClick={() => {
  //             dispatch(changeState())
  //             dispatch(changeLoadingFiltersState())
  //             let asideFilters = {} as typeof asideItemConf;
  //             let key: keyof AsideFiltersInterface;
  //             for (key in asideItemConf) {
  //               asideFilters[key] = [...asideItemConf[key]]
  //             }
  //             const fieldList = fieldName as keyof typeof asideItemConf;
  //             const value = document.value
  //             const index = asideFilters[fieldList].indexOf(value, 0);
  //             if (index > -1) {
  //               asideFilters[fieldList].splice(index, 1);
  //             }
  //             else {
  //               asideFilters[fieldList].push(value)
  //             }
  //             dispatch(reset())
  //             dispatch(changeLoadingHorizontalFiltersState())
  //             dispatch(setAsideItemConfiguration({updateAsideItemConfig:asideFilters}))
  //             dispatch(updateChangeType({newChange: 'asideItem'}))
  //             // dispatch(updateChangeType({newChange: 'horizontalItem'}))
  //             dispatch(setSearchState({searchingState:false}))
  //             toggleButtonHandler();
  //             }
  //           }
  //         >
  //           <AsideMenuItemWithSub
  //             to='/crafted/pages'
  //             title={document.value.concat(' (' + document.count.toString() + ')')}
  //             fontIcon='bi-archive'
  //           >
              
  //           </AsideMenuItemWithSub>
  //       </a> 
  //   )
  // }
    
  const ShowAsideElementsHandler: React.FC<PropsDocs> = ({asideDocuments, listFieldName}) => { 
      return (
        <>
          <ul>
            {asideDocuments?.slice(0,3).map((doc, index) => (
              <ShowAsideItemHandler document={doc} idx={index} fieldName={listFieldName} key={index}/>
            ))}
          </ul>
          
          {
            asideDocuments?.length > 3 &&
            <div className="accordion" id={"kt_accordion_1" + listFieldName}>
              <div className="accordion-item">
                <h2 className="accordion-header " id={"kt_accordion_1_header_1" + listFieldName}>
                    <button 
                      className="accordion-button fs-7 fw-bold" 
                      type="button" 
                      data-bs-toggle="collapse" 
                      data-bs-target={"#kt_accordion_1_body_1" + listFieldName} 
                      aria-expanded="true" aria-controls={"kt_accordion_1_body_1" + listFieldName}
                      style={{paddingLeft:'50px'}}
                    >
                      . . .
                    </button>
                </h2>
                <div id={"kt_accordion_1_body_1" + listFieldName} className="accordion-collapse collapse show" aria-labelledby={"kt_accordion_1_header_1" + listFieldName} data-bs-parent={"#kt_accordion_1" + listFieldName}>
                  <ul>
                    {asideDocuments?.slice(3).map((doc, index) => (
                      <ShowAsideItemHandler document={doc} idx={index} fieldName={listFieldName} key={index}/> 
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          }
        </>
      );
  }

  if (currentFiltersChangeStatus){
    const newData = updateFiltersHandler();
    dispatch(changeLoadingFiltersState())
  }

  return (
    <>
      <AsideCheckBox/>
      <AsideCheckBox2/>
      {loadedDocuments.ext?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Endung</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.ext} listFieldName='ext'/>
      </>
      } 

      {loadedDocuments.Außenanlagen?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Außenanlagen</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Außenanlagen} listFieldName='Außenanlagen'/>
      </>
      }
      
      {loadedDocuments.Baumaßnahme?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Baumaßnahme</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Baumaßnahme} listFieldName='Baumaßnahme'/>
      </>
      } 

      {loadedDocuments.Bepflanzungen?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Bepflanzungen</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Bepflanzungen} listFieldName='Bepflanzungen'/>
      </>
      } 

      {loadedDocuments.Brandschutz?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Brandschutz</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Brandschutz} listFieldName='Brandschutz'/>
      </>
      } 

      {loadedDocuments.Dach?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Dach</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Dach} listFieldName='Dach'/>
      </>
      } 

      {loadedDocuments.Denkmalart?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Denkmalart</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Denkmalart} listFieldName='Denkmalart'/>
      </>
      } 

      {loadedDocuments.Denkmalname?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Denkmalname</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Denkmalname} listFieldName='Denkmalname'/>
      </>
      } 

      {loadedDocuments.Diverse?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Diverse</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Diverse} listFieldName='Diverse'/>
      </>
      } 

      {loadedDocuments.Eingangsbereich?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Eingangsbereich</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Eingangsbereich} listFieldName='Eingangsbereich'/>
      </>
      } 

      {loadedDocuments.Farbe?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Farbe</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Farbe} listFieldName='Farbe'/>
      </>
      } 

      {loadedDocuments.Fassade?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Fassade</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Fassade} listFieldName='Fassade'/>
      </>
      } 

      {loadedDocuments.Fenster?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Fenster</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Fenster} listFieldName='Fenster'/>
      </>
      } 

      {loadedDocuments.Funk?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Funk</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Funk} listFieldName='Funk'/>
      </>
      } 

      {loadedDocuments.Gebäude?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Gebäude</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Gebäude} listFieldName='Gebäude'/>
      </>
      } 

      {loadedDocuments.Gebäudenutzung?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Gebäudenutzung</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Gebäudenutzung} listFieldName='Gebäudenutzung'/>
      </>
      } 

      {loadedDocuments.Haustechnik?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Haustechnik</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Haustechnik} listFieldName='Haustechnik'/>
      </>
      } 

      {loadedDocuments.Kunst?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Kunst</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Kunst} listFieldName='Kunst'/>
      </>
      } 

      {loadedDocuments.Maßnahme?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Maßnahme</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Maßnahme} listFieldName='Maßnahme'/>
      </>
      } 

      {loadedDocuments.Nutzungsänderung?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Nutzungsänderung</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Nutzungsänderung} listFieldName='Nutzungsänderung'/>
      </>
      } 

      {loadedDocuments.Sachbegriff?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Sachbegriff</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Sachbegriff} listFieldName='Sachbegriff'/>
      </>
      } 

      {loadedDocuments.Solaranlage?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Solaranlage</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Solaranlage} listFieldName='Solaranlage'/>
      </>
      } 

      {loadedDocuments.Treppenhaus?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Treppenhaus</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Treppenhaus} listFieldName='Treppenhaus'/>
      </>
      } 

      {loadedDocuments.Tür?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Tür</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Tür} listFieldName='Tür'/>
      </>
      } 

      {loadedDocuments.Werbeanlage?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Werbeanlage</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.Werbeanlage} listFieldName='Werbeanlage'/>
      </>
      } 

      {loadedDocuments.district?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>District</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.district} listFieldName='district'/>
      </>
      } 

      {/* {loadedDocuments.doctype?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>DocType</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.doctype} listFieldName='doctype'/>
      </>
      }  */}

      {loadedDocuments.hidas?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Hidas</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.hidas} listFieldName='hidas'/>
      </>
      }    

      {loadedDocuments.path?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Path</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.path} listFieldName='path'/>
      </>
      } 

      {loadedDocuments.vorhaben?.length > 0 && 
      <>
        <div className='menu-item'>
          <div className='menu-content pt-8 pb-2'>
            <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Vorhaben</span>
          </div>
        </div>
        <ShowAsideElementsHandler asideDocuments={loadedDocuments.vorhaben} listFieldName='vorhaben'/>
      </>
      } 

    </>
  )
  
}
