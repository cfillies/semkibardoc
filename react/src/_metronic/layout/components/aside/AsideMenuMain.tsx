/* eslint-disable react/jsx-no-target-blank */
import React, { useEffect, useState } from 'react'
import {useIntl} from 'react-intl'
import {KTSVG} from '../../../helpers'
import {AsideMenuItemWithSub} from './AsideMenuItemWithSub'
import {AsideMenuItem} from './AsideMenuItem'
import AsideCheckBox from './AsideCheckBox'
import AsideCheckBox2 from './AsideCheckBox2'
import { AsideMenuInterface } from '../../../../utils/interfaces'
import { useDispatch, useSelector } from 'react-redux'
import { changeState, updateChangeType, setAsideItemConfiguration } from '../../../../features/filter/filterObjectSlice'
import { InnerAsideMenuInterface } from '../../../../utils/interfaces'


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
  const [isLoading, setIsLoading] = useState(true);
  const [loadedDocuments, setLoadedDocuments] = useState<AsideMenuInterface>({} as AsideMenuInterface);
  const [loadedDocumentsCounter, setLoadedDocumentsCounter] = useState<number>(0);
  const [itemsNumberToShow, setItemsNumberToShow] = useState<number>(3);

  const dispatch = useDispatch()
  
  useEffect(() => {
    setIsLoading(true);
    fetch(
      'http://localhost:5000/aside/'
    )
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        // console.log(doc_list)
        setIsLoading(false);
        setLoadedDocuments(data[0]);
       
      });
  }, []);

  if (isLoading) {
    return (
      <section>
        <p>Loading...</p>
      </section>
    );
  }

  // function FirstThreeElementsHandler(document:InnerAsideMenuInterface, idx: number, fieldName: string) {
  
  const FirstThreeElementsHandler: React.FC<Props> = ({document, idx, fieldName}) => {
    return (
      <ul>
            <a 
              href="#"
              key={fieldName + '_link' + idx.toString()}  
              onClick={() => {
                dispatch(changeState())
                dispatch(setAsideItemConfiguration({updateAsideItemConfig: {fieldName: fieldName, valueField: document._id}}))
                dispatch(updateChangeType({newChange: 'asideItem'}))
                }
              }
            >
              
                <AsideMenuItemWithSub
                
                to='/crafted/pages'
                title={document._id.concat(' (' + document.count.toString() + ')')}
                fontIcon='bi-archive'
                
                key={fieldName + '_' + idx.toString()} 
                >
                  
                </AsideMenuItemWithSub>
            
            </a> 
          </ul>
    )
  }
  
  // function AfterThreeElementsHandler(document:InnerAsideMenuInterface, idx: number, fieldName: string) {
    const AfterThreeElementsHandler: React.FC<Props> = ({document, idx, fieldName}) => {
     return (
     
        <ul>
          <a 
            href="#"
            key={fieldName + '_link' + idx.toString()}  
            onClick={() => {
              dispatch(changeState())
              dispatch(setAsideItemConfiguration({updateAsideItemConfig: {fieldName: fieldName, valueField: document._id}}))
              dispatch(updateChangeType({newChange: 'asideItem'}))
              }
            }
          >
            <div className="accordion-body">
              {document._id.concat(' (' + document.count.toString() + ')')}
            </div>
          </a>
        </ul>
               
      )
  }

  // function ShowElementsHandler(document:InnerAsideMenuInterface, idx: number, fieldName: string) {
  const ShowElementsHandler: React.FC<Props> = ({document, idx, fieldName}) => { 
   
    if (idx < 3) {
      return <FirstThreeElementsHandler document={document} idx={idx} fieldName={fieldName} />;
    }
    else {
      return (
        <div className="accordion" id="kt_accordion_1">
          <div className="accordion-item">
            <h2 className="accordion-header" id="kt_accordion_1_header_1">
                <button className="accordion-button fs-7 fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#kt_accordion_1_body_1" aria-expanded="true" aria-controls="kt_accordion_1_body_1">
                  Zeig mehr
                </button>
            </h2>
              <div id="kt_accordion_1_body_1" className="accordion-collapse collapse show" aria-labelledby="kt_accordion_1_header_1" data-bs-parent="#kt_accordion_1">
                <AfterThreeElementsHandler document={document} idx={idx} fieldName={fieldName} />
                </div>
            </div>
          </div> 
          );
    }
  }

  // const ShowAsideElementsHandler: React.FC<PropsDocs> = ({asideDocuments, listFieldName}) => { 
   
  //   if (idx < 3) {
  //     return <FirstThreeElementsHandler document={document} idx={idx} fieldName={fieldName} />;
  //   }
  //   else {
  //     return (
  //       <div className="accordion" id="kt_accordion_1">
  //         <div className="accordion-item">
  //           <h2 className="accordion-header" id="kt_accordion_1_header_1">
  //               <button className="accordion-button fs-7 fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#kt_accordion_1_body_1" aria-expanded="true" aria-controls="kt_accordion_1_body_1">
  //                 Zeig mehr
  //               </button>
  //           </h2>
  //             <div id="kt_accordion_1_body_1" className="accordion-collapse collapse show" aria-labelledby="kt_accordion_1_header_1" data-bs-parent="#kt_accordion_1">
  //               <AfterThreeElementsHandler document={document} idx={idx} fieldName={fieldName} />
  //               </div>
  //           </div>
  //         </div> 
  //         );
  //   }
  // }
  
  const ShowAsideElementsHandler: React.FC<PropsDocs> = ({asideDocuments, listFieldName}) => { 
    
      asideDocuments?.map((doc, index) => (
        <FirstThreeElementsHandler document={doc} idx={index} fieldName={listFieldName}/>
      )
      )
   
    }
    

    
 

  return (
    <>
      <AsideCheckBox/>
      <AsideCheckBox2/>

      <div className='menu-item'>
        <div className='menu-content pt-8 pb-2'>
          <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Vorhaben</span>
        </div>
      </div>

        
          
          <ShowAsideElementsHandler asideDocuments={loadedDocuments.vorhaben?.slice(0,3)} listFieldName='vorhaben'/>

          <div className="accordion" id="kt_accordion_1">
          <div className="accordion-item">
            <h2 className="accordion-header" id="kt_accordion_1_header_1">
                <button className="accordion-button fs-7 fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#kt_accordion_1_body_1" aria-expanded="true" aria-controls="kt_accordion_1_body_1">
                  Zeig mehr
                </button>
            </h2>
              <div id="kt_accordion_1_body_1" className="accordion-collapse collapse show" aria-labelledby="kt_accordion_1_header_1" data-bs-parent="#kt_accordion_1">
              <ShowAsideElementsHandler asideDocuments={loadedDocuments.vorhaben?.slice(3)} listFieldName='vorhaben'/>
                </div>
            </div>
          </div> 
      

      <div className='menu-item'>
        <div className='menu-content pt-8 pb-2'>
          <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Objektnummer</span>
        </div>
      </div>
      <ul>
        {loadedDocuments.objektnummer?.map((doc, index) => (
          <a 
            href="#"
            key={'hidas_link' + index.toString()}  
            onClick={() => {
              dispatch(changeState())
              dispatch(setAsideItemConfiguration({updateAsideItemConfig: {fieldName: 'hidas', valueField: doc._id}}))
              dispatch(updateChangeType({newChange: 'asideItem'}))
              }
            }
          >
            <AsideMenuItemWithSub
            to='/crafted/pages'
            title={doc._id.concat(' (' + doc.count.toString() + ')')}
            fontIcon='bi-archive'
            key={'hidas_' + index.toString()} 
            >
            </AsideMenuItemWithSub>
        </a> 
        ))}
      </ul>

      <div className='menu-item'>
        <div className='menu-content pt-8 pb-2'>
          <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Sachbegriffe</span>
        </div>
      </div>
      <ul>
          {loadedDocuments.sachbegriff?.map((doc, index) => (
            <a 
              href="#" 
              key={'Sachbegriff_link' + index.toString()} 
              onClick={() => {
                dispatch(changeState())
                dispatch(setAsideItemConfiguration({updateAsideItemConfig: {fieldName: 'Sachbegriff', valueField: doc._id}}))
                dispatch(updateChangeType({newChange: 'asideItem'}))
                }
              }
            >
              <AsideMenuItemWithSub
              to='/crafted/pages'
              title={doc._id.concat(' (' + doc.count.toString() + ')')}
              fontIcon='bi-archive'
              key={'Sachbegriff_' + index.toString()} 
              >
              </AsideMenuItemWithSub>
          </a> 
          ))}
        </ul>

      <div className='menu-item'>
        <div className='menu-content pt-8 pb-2'>
          <span className='menu-section text-muted text-uppercase fs-8 ls-1'>Denkmalart</span>
        </div>
      </div>
      <ul>
          {loadedDocuments.denkmalart?.map((doc, index) => (
            <a 
              href="#" 
              key={'Denkmalart_link' + index.toString()} 
              onClick={() => {
                dispatch(changeState())
                dispatch(setAsideItemConfiguration({updateAsideItemConfig: {fieldName: 'Denkmalart', valueField: doc._id}}))
                dispatch(updateChangeType({newChange: 'asideItem'}))
                }
              }
            >
              <AsideMenuItemWithSub
              to='/crafted/pages'
              title={doc._id.concat(' (' + doc.count.toString() + ')')}
              fontIcon='bi-archive'
              key={'Denkmalart_' + index.toString()} 
              >
              </AsideMenuItemWithSub>
          </a> 
          ))}
        </ul>

      <div className='menu-item'>
        <div className='menu-content'>
          <div className='separator mx-1 my-4'></div>
        </div>
      </div>

    </>
  )
}
