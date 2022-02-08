import React, {FC, useEffect, useState} from 'react'
import {
  ListsWidget7,
} from '../../../../_metronic/partials/widgets'

import { useDispatch, useSelector } from 'react-redux'
import { fetchDocumentsAsync, docList, fetchStatus, searchDocumentsAsync, fetchItemFieldAsync } from '../../../../features/filter/documentsSlice'
import { setNewFilter, newFilter, changeState, currentState, currentChangeType, searchConfigurations, asideItemConfigurations } from '../../../../features/filter/filterObjectSlice'
import { setTotalPagesNumber } from '../../../../features/filter/totalPagesSlice'
import { FilterInterface } from '../../../../utils/interfaces'

interface DocumentsInterface {
  id: number,
  file: string,
  path: string,
  doctype: string,
  adresse: string,
  hidas: string,
  denkmalart: string,
  doc_image: string,
}

interface FetchedJSON {
  type: string,
  payload: any[],
  meta: any
}

const booleanFilterArray: FilterInterface = 
  {"Antrag": true,
  "Eigangsbestätigung": true,
  "Genehmigung": true,
  "Versagung": true,
  "Stellungnahme": true,
  "Anhorungrag": true,
  "from": 0,
  "size": 10
}

const DUMMY_DATA = [
  {
    id: 1,
    file: 'file1',
    path: 'doc_order1',
    doctype: 'doc_type1',
    adresse: 'doc_address1',
    hidas: 'doc_obj_nr1',
    denkmalart: 'denkmalart1',
    doc_image: 'doc_image1',
  },
  {
    id: 2,
    file: 'file2',
    path: 'doc_order2',
    doctype: 'doc_type2',
    adresse: 'doc_address2',
    hidas: 'doc_obj_nr2',
    denkmalart: 'denkmalart2',
    doc_image: 'doc_image2',
  },
];

const Lists: FC = () => {

  const dispatch = useDispatch()
  const currentStatus = useSelector(fetchStatus)
  const currentChangeStatus = useSelector(currentState)
  const updatedFilter: FilterInterface = useSelector(newFilter);
  const changeType = useSelector(currentChangeType)
  const searchConf = useSelector(searchConfigurations)
  const asideItemConf = useSelector(asideItemConfigurations)

  const [isLoading, setIsLoading] = useState(true);
  const [loadedDocuments, setLoadedDocuments] = useState<DocumentsInterface[]>([]);


  const updateDocumentsListHandler = async () => {
    console.log("onSavePostClicked");
    if (changeType === 'filtering' || changeType == 'newPage') {
      try {
        const t = await dispatch(fetchDocumentsAsync(updatedFilter));
        let jsonResult = JSON.stringify(t);
        let objResult = JSON.parse(jsonResult);
        // console.log(objResult.payload);

        const totalNumberOfDocs = objResult.payload[objResult.payload.length - 1]["totalNumberOfDocuments"]
        dispatch(setTotalPagesNumber({docsNumber: totalNumberOfDocs, pageSize: 5}))

        const doc_list = [];
        for (const key in objResult.payload.slice(0, -1)) {
          const doc = {
            id: key,
            ...objResult.payload[key]
          };
    
          doc_list.push(doc);
        }
        setLoadedDocuments(doc_list);
      } 
      catch (err) {
        console.error('Failed to save the post: ', err)
      } 
    }

    else if (changeType === 'searching' ) {
      console.log('Searching')
      try {
        const t = await dispatch(searchDocumentsAsync(searchConf));

        let jsonResult = JSON.stringify(t);
        let objResult = JSON.parse(jsonResult);
        console.log(objResult.payload);

        let totalNumberOfDocs = 0;
        if (objResult.payload[0].count.length !== 0) {
          totalNumberOfDocs = objResult.payload[0].count[0].total
        }
        
        dispatch(setTotalPagesNumber({docsNumber: totalNumberOfDocs, pageSize: 5}))

        const doc_list = [];
        for (const key in objResult.payload[0].fetchedDocuments) {
          const doc = {
            id: key,
            ...objResult.payload[0].fetchedDocuments[key]
          };
    
          doc_list.push(doc);
        }
        setLoadedDocuments(doc_list);
      } 
      catch (err) {
        console.error('Failed to save the post: ', err)
      } 
    }

    else if (changeType === 'asideItem' ) {
      try {
        const t = await dispatch(fetchItemFieldAsync(asideItemConf));

        let jsonResult = JSON.stringify(t);
        let objResult = JSON.parse(jsonResult);
        console.log(objResult.payload);

        const totalNumberOfDocs = objResult.payload[objResult.payload.length - 1]["totalNumberOfDocuments"]
        dispatch(setTotalPagesNumber({docsNumber: totalNumberOfDocs, pageSize: 5}))

        const doc_list = [];
        for (const key in objResult.payload.slice(0, -1)) {
          const doc = {
            id: key,
            ...objResult.payload[key]
          };
    
          doc_list.push(doc);
        }
        setLoadedDocuments(doc_list);
      } 
      catch (err) {
        console.error('Failed to save the post: ', err)
      } 
    }
    
  }

  

  // useEffect(() => {
  //   setIsLoading(true);
  //   fetch(
  //     'http://localhost:5000/record/'
  //   )
  //     .then((response) => {
  //       return response.json();
  //     })
  //     .then((data) => {
  //       const doc_list = [];

  //       for (const key in data) {
  //         const doc = {
  //           id: key,
  //           ...data[key]
  //         };

  //         doc_list.push(doc);
  //       }

  //       // console.log(doc_list)
  //       setIsLoading(false);
  //       setLoadedDocuments(doc_list);
  //       dispatch(changeState())
  //     });
  // }, []);

  // if (isLoading) {
  //   return (
  //     <section>
  //       <p>Loading...</p>
  //     </section>
  //   );
  // }

  
  if (currentChangeStatus){
    // setLoadedDocuments([]);
    const newData = updateDocumentsListHandler();
    dispatch(changeState())
    // console.log(newData)
  }

  return (
    <>
    {/* <div className='row g-5 g-xl-8'> */}
      
      {/* <div className='col-xl-15'> */}
      {/* <a href="#" className="btn btn-primary" onClick={onSavePostClicked} >Primary</a> */}
        <ListsWidget7 className='card-xl-stretch mb-xl-8' 
                      data-kt-scroll='true'
                      data-kt-scroll-activate='{default: false, lg: true}'
                      data-kt-scroll-height='auto'
                      data-kt-scroll-wrappers='#kt_aside_menu'
                      data-kt-scroll-offset='0'
                      // docs={DUMMY_DATA}
                      docs={loadedDocuments}
        />
      {/* </div>
    </div> */}
    </>
  )
}

export {Lists}
