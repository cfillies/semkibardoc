import {FC, useState} from 'react'
import {
  ListsWidget7,
} from '../../../../_metronic/partials/widgets'

import { useDispatch, useSelector } from 'react-redux'
import { fetchDocumentsAsync, searchDocumentsAsync, fetchItemFieldAsync } from '../../../../features/filter/documentsSlice'
import { currentSearchState, newFilter, changeState, currentState, currentChangeType, searchConfigurations, asideFiltersConfigurations } from '../../../../features/filter/filterObjectSlice'
import { setTotalPagesNumber } from '../../../../features/filter/totalPagesSlice'
import { FilterInterface } from '../../../../utils/interfaces'
import {currentPageSize} from '../../../../features/filter/counterSlice'

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

// const DUMMY_DATA = [
//   {
//     id: 1,
//     file: 'file1',
//     path: 'doc_order1',
//     doctype: 'doc_type1',
//     adresse: 'doc_address1',
//     hidas: 'doc_obj_nr1',
//     denkmalart: 'denkmalart1',
//     doc_image: 'doc_image1',
//   },
//   {
//     id: 2,
//     file: 'file2',
//     path: 'doc_order2',
//     doctype: 'doc_type2',
//     adresse: 'doc_address2',
//     hidas: 'doc_obj_nr2',
//     denkmalart: 'denkmalart2',
//     doc_image: 'doc_image2',
//   },
// ];

const Lists: FC = () => {

  const dispatch = useDispatch()
  const currentSearchingStatus = useSelector(currentSearchState)
  const currentChangeStatus = useSelector(currentState)
  const updatedFilter: FilterInterface = useSelector(newFilter);
  const changeType = useSelector(currentChangeType)
  const searchConf = useSelector(searchConfigurations)
  const asideItemConf = useSelector(asideFiltersConfigurations)
  const thisPageSize = useSelector(currentPageSize)

  const [loadedDocuments, setLoadedDocuments] = useState<DocumentsInterface[]>([]);


  const updateDocumentsListHandler = async () => {
    if (changeType === 'filtering' && !currentSearchingStatus) {
      try {
        const t = await dispatch(fetchDocumentsAsync(updatedFilter));
        let jsonResult = JSON.stringify(t);
        let objResult = JSON.parse(jsonResult);
        // console.log(objResult.payload);

        // const totalNumberOfDocs = objResult.payload[objResult.payload.length - 1]["totalNumberOfDocuments"]
        const totalNumberOfDocs = objResult.payload.count
        dispatch(setTotalPagesNumber({docsNumber: totalNumberOfDocs, pageSize: thisPageSize}))

        const doc_list = [];
        for (const key in objResult.payload.metadata) {
          const doc = {
            id: key,
            ...objResult.payload.metadata[key]
          };
    
          doc_list.push(doc);
        }
        setLoadedDocuments(doc_list);
      } 
      catch (err) {
        console.error('Failed to load documents: ', err)
      } 
    }

    else if ((changeType === 'searching' || changeType === 'newPage') && currentSearchingStatus) {
      // console.log('Searching')
      try {
        const t = await dispatch(searchDocumentsAsync(searchConf));

        let jsonResult = JSON.stringify(t);
        let objResult = JSON.parse(jsonResult);
        console.log(objResult.payload);

        // let totalNumberOfDocs = 0;
        // for (let key in objResult.payload) {
        //   totalNumberOfDocs += objResult.payload[key].length
        // }
        const totalNumberOfDocs = objResult.payload.count
                
        dispatch(setTotalPagesNumber({docsNumber: totalNumberOfDocs, pageSize: thisPageSize}))

        const doc_list = [];
        for (const key in objResult.payload.metadata) {
          const doc = {
            id: key,
            ...objResult.payload.metadata[key]
          };
    
          doc_list.push(doc);
        }
        setLoadedDocuments(doc_list);
      } 
      catch (err) {
        console.error('Failed to save the post: ', err)
      } 
    }

    else if ((changeType === 'asideItem' || changeType === 'newPage' ) && !currentSearchingStatus) {
      // console.log(asideItemConf)
      try {
        const t = await dispatch(fetchItemFieldAsync(asideItemConf));

        let jsonResult = JSON.stringify(t);
        let objResult = JSON.parse(jsonResult);

        const totalNumberOfDocs = objResult.payload.count
        dispatch(setTotalPagesNumber({docsNumber: totalNumberOfDocs, pageSize: thisPageSize}))

        const doc_list = [];
        for (const key in objResult.payload.metadata) {
          const doc = {
            id: key,
            ...objResult.payload.metadata[key]
          };
    
          doc_list.push(doc);
        }
        setLoadedDocuments(doc_list);
      } 
      catch (err) {
        console.error('Failed to fetch documents: ', err)
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
