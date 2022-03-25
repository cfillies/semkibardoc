import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { string } from 'yup/lib/locale';
import type { RootState } from '../../setup/redux/Store'
import store from '../../setup/redux/Store';
import { AsideFiltersInterface, AsideMatchFiltersInterface } from '../../utils/interfaces';

interface FilterInterface {
  "Antrag": boolean,
  "Eigangsbestätigung": boolean,
  "Genehmigung": boolean,
  "Versagung": boolean,
  "Stellungnahme": boolean,
  "Anhorungrag": boolean,
  "page": number,
  "page_size": number
}

interface SearchInterface {
  "field": string,
  "search": string
}

interface documentsState {
  

  // Multiple possible status enum values
  status: 'idle' | 'loading' | 'succeeded' | 'failed',
  docTypStatus: 'idle' | 'loading' | 'succeeded' | 'failed',
  error: string | null
  
}

const initialState: documentsState = {
    
    status: 'idle',
    docTypStatus: 'idle',
    error: null
  }

export const fetchDocumentsAsync = createAsyncThunk(
    'documents/fetchDocumentsAsync', 
    async (filtersObject: FilterInterface) => {
        let request = "page="+(store.getState().counter.value - 1).toString()+"&";
        request += "page_size="+store.getState().counter.pageSize.toString();
        // let req = 'http://localhost:5000/search/resolved2?';
        let req = `${process.env.REACT_APP_API_URL}/search/resolved2?`
        req+=request
        const response = await fetch(req);
        return await (response.json()) as JSON
    }
)

export const searchDocumentsAsync = createAsyncThunk(
  'documents/searchDocumentsAsync', 
  async (filtersObject: SearchInterface) => {
    let request = "page="+(store.getState().counter.value - 1).toString()+"&";
    request += "page_size="+store.getState().counter.pageSize.toString() + "&search=";
    const searchQueryArray = filtersObject.search.split(' ')
    const searchQuery = searchQueryArray.join("+")
    request += searchQuery;
    // let req = 'http://localhost:5000/search/resolved2?';
    let req = `${process.env.REACT_APP_API_URL}/search/resolved2?`
    req+=request
    const response = await fetch(req);
    return await (response.json()) as JSON
  }
)

export const searchFiltersAsync = createAsyncThunk(
  'documents/searchFiltersAsync', 
  async (filtersObject:SearchInterface) => {
    
    let request = "search=";
    const searchQueryArray = filtersObject.search.split(' ')
    const searchQuery = searchQueryArray.join("+")
    request += searchQuery;
    // let req = 'http://localhost:5000/search/resolved2_facets?';
    let req = `${process.env.REACT_APP_API_URL}/search/resolved2_facets?`
    req+=request
    const response = await fetch(req);
    return await (response.json()) as JSON
  }
)

export const fetchItemFieldAsync = createAsyncThunk(
  'documents/fetchItemFieldAsync', 
  async (filtersObject:{filterQuery: AsideFiltersInterface, searchQuery: SearchInterface}) => {
    let request = "page="+(store.getState().counter.value - 1).toString()+"&";
    request += "page_size="+store.getState().counter.pageSize.toString()+"&";
    if (filtersObject.searchQuery.search.length > 0) {
      request += "search="
      const searchQueryArray = filtersObject.searchQuery.search.split(' ')
      const searchQuery = searchQueryArray.join("+")
      request += searchQuery+"&";
    }
      let key: keyof AsideFiltersInterface;
      for (key in filtersObject.filterQuery){
        if (filtersObject.filterQuery[key].length > 0) {
          request+=key.toString();
          request+="=";
          for (let idx = 0; idx < filtersObject.filterQuery[key].length; idx++) {
            request+=filtersObject.filterQuery[key][idx];
            request+=",";
          }
          request = request.slice(0,-1);
          request+="&";
        }
      }
      // let req = 'http://localhost:5000/search/resolved2?'
      let req = `${process.env.REACT_APP_API_URL}/search/resolved2?`
      if (request.endsWith("&")) {
        req += request.slice(0,-1);
      }
      else {
        req+=request
      }
      
      const response = await fetch(req);
      // console.log(response.json())
      return await (response.json()) as JSON
  }
)

export const fetchFilters = createAsyncThunk(
  'documents/fetchFilters', 
  async (filtersObject:{filterQuery: AsideFiltersInterface, searchQuery: SearchInterface}) => {
    let request = "";
    if (filtersObject.searchQuery.search.length > 0) {
      request += "search="
      const searchQueryArray = filtersObject.searchQuery.search.split(' ')
      const searchQuery = searchQueryArray.join("+")
      request += searchQuery + "&";
    }
    let key: keyof AsideFiltersInterface;
    for (key in filtersObject.filterQuery){
      if (filtersObject.filterQuery[key].length > 0) {
        request+=key.toString();
        request+="=";
        for (let idx = 0; idx < filtersObject.filterQuery[key].length; idx++) {
          request+=filtersObject.filterQuery[key][idx];
          request+=",";
        }
        request = request.slice(0,-1);
        request+="&";
      }
      
    }
    // let req = 'http://localhost:5000/search/resolved2_facets?'
    let req = `${process.env.REACT_APP_API_URL}/search/resolved2_facets?`
    if (request.endsWith("&")) {
      req+=request.slice(0,-1);
    }
    else {
      req += request
    }
    const response = await fetch(req);
    return await (response.json()) as JSON
  }
)

export const fetchItemsWithPostMethodAsync = createAsyncThunk(
  'documents/fetchItemsWithPostMethodAsync', 
  async (filtersObject:{filterQuery: AsideFiltersInterface, searchQuery: SearchInterface}) => {
    const page = store.getState().counter.value - 1;
    const page_size = store.getState().counter.pageSize
    const search = filtersObject.searchQuery.search.length > 0? filtersObject.searchQuery.search: "";
    let match = {} as AsideMatchFiltersInterface
    let request = "page=" + (store.getState().counter.value - 1).toString() + "&";
    request += "page_size=" + store.getState().counter.pageSize.toString() + "&";

    let key: keyof AsideFiltersInterface;
    for (key in filtersObject.filterQuery){
      if (filtersObject.filterQuery[key].length > 0) {
        let filterArray = []
        for (let idx = 0; idx < filtersObject.filterQuery[key].length; idx++) {
          request+=filtersObject.filterQuery[key][idx];
          filterArray.push(filtersObject.filterQuery[key][idx])
        }
        match[key] = {"$in": filterArray}
      }
    }
    const data = {
      "page": page,
      "page_size": page_size,
      "search": search,
      "match": match,
      "categories": ["Außenanlagen", "Baumaßnahme", "Bepflanzungen", "Brandschutz","Dach", "Diverse", "Eingangsbereich", "Farbe", "Fassade", "Gebäude", "Gebäudenutzung", "Haustechnik", "Maßnahme", "Nutzungsänderung", "Werbeanlage"],
      "singlevaluefacets": ["path", "doctype", "ext", "district", "vorhaben"],
      "multivaluefacets": ["hidas", "Sachbegriff", "Denkmalart", "Denkmalname"]
    }
    let uri = `${process.env.REACT_APP_API_URL}/search/metadata_facets?`
          
    const response = await fetch(uri, {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    
      body: JSON.stringify(
        data
      )
    });
    // console.log(data)
    // console.log(response.json())
    return await (response.json()) as JSON
  }
)

export const fetchDocumentsWithPostMethodAsync = createAsyncThunk(
  'documents/fetchDocumentsWithPostMethodAsync', 
  async (filtersObject:{filterQuery: AsideFiltersInterface, searchQuery: SearchInterface}) => {
    const page = store.getState().counter.value - 1;
    const page_size = store.getState().counter.pageSize
    const search = filtersObject.searchQuery.search.length > 0? filtersObject.searchQuery.search: "";
    let match = {} as AsideMatchFiltersInterface
    
    let key: keyof AsideFiltersInterface;
    for (key in filtersObject.filterQuery){
      if (filtersObject.filterQuery[key].length > 0) {
        let filterArray = []
        for (let idx = 0; idx < filtersObject.filterQuery[key].length; idx++) {
          filterArray.push(filtersObject.filterQuery[key][idx])
        }
        match[key] = {"$in": filterArray}
      }
    }
    const data = {
      "page": page,
      "page_size": page_size,
      "search": search,
      "match": match,
      "categories": ["Außenanlagen", "Baumaßnahme", "Bepflanzungen", "Brandschutz","Dach", "Diverse", "Eingangsbereich", "Farbe", "Fassade", "Gebäude", "Gebäudenutzung", "Haustechnik", "Maßnahme", "Nutzungsänderung", "Werbeanlage"],
      "singlevaluefacets": ["path", "doctype", "ext", "district", "vorhaben"],
      "multivaluefacets": ["hidas", "Sachbegriff", "Denkmalart", "Denkmalname"]
    }
    let uri = `${process.env.REACT_APP_API_URL}/search/metadata?`
          
    const response = await fetch(uri, {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    
      body: JSON.stringify(
        data
      )
    });
    // console.log(data)
    // console.log(response.json())
    return await (response.json()) as JSON
  }
)

export const slice = createSlice({
  name: 'allFetchedDocuments',
  initialState,
  reducers: {
  },
  extraReducers: builder => {
    builder
      .addCase(fetchDocumentsAsync.pending, (state, action) => {
        state.status = 'loading'
      })
      .addCase(fetchDocumentsAsync.fulfilled, (state, action) => {
        state.status = 'succeeded'
      })
      .addCase(fetchDocumentsAsync.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message as keyof typeof string
      })
      .addCase(searchDocumentsAsync.pending, (state, action) => {
        state.status = 'loading'
      })
      .addCase(searchDocumentsAsync.fulfilled, (state, action) => {
        state.status = 'succeeded'
      })
      .addCase(searchDocumentsAsync.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message as keyof typeof string
      })
      .addCase(fetchItemFieldAsync.pending, (state, action) => {
        state.status = 'loading'
      })
      .addCase(fetchItemFieldAsync.fulfilled, (state, action) => {
        state.status = 'succeeded'
      })
      .addCase(fetchItemFieldAsync.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message as keyof typeof string
      })
      .addCase(fetchFilters.pending, (state, action) => {
        state.docTypStatus = 'loading'
      })
      .addCase(fetchFilters.fulfilled, (state, action) => {
        state.docTypStatus = 'succeeded'
      })
      .addCase(fetchFilters.rejected, (state, action) => {
        state.docTypStatus = 'failed'
        state.error = action.error.message as keyof typeof string
      })
      .addCase(searchFiltersAsync.pending, (state, action) => {
        state.docTypStatus = 'loading'
      })
      .addCase(searchFiltersAsync.fulfilled, (state, action) => {
        state.docTypStatus = 'succeeded'
      })
      .addCase(searchFiltersAsync.rejected, (state, action) => {
        state.docTypStatus = 'failed'
        state.error = action.error.message as keyof typeof string
      })
      .addCase(fetchItemsWithPostMethodAsync.pending, (state, action) => {
        state.docTypStatus = 'loading'
      })
      .addCase(fetchItemsWithPostMethodAsync.fulfilled, (state, action) => {
        state.docTypStatus = 'succeeded'
      })
      .addCase(fetchItemsWithPostMethodAsync.rejected, (state, action) => {
        state.docTypStatus = 'failed'
        state.error = action.error.message as keyof typeof string
      })
      .addCase(fetchDocumentsWithPostMethodAsync.pending, (state, action) => {
        state.status = 'loading'
      })
      .addCase(fetchDocumentsWithPostMethodAsync.fulfilled, (state, action) => {
        state.status = 'succeeded'
      })
      .addCase(fetchDocumentsWithPostMethodAsync.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message as keyof typeof string
      })
  }
});


// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched
// export const incrementAsync = amount => dispatch => {
//   setTimeout(() => {
//     dispatch(incrementByAmount(amount));
//   }, 1000);
// };

// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.counter.value)`

// export const fetchedDocuments = state => state.fetchedDocuments.value;
// export const allFetchedDocuments = state => state.fetchedDocuments.documentsList;

export const fetchStatus = (state: RootState) => state.documentsSlice.status;
export const docTypFilterStatus = (state: RootState) => state.documentsSlice.docTypStatus;
// const lastReturnedAction = await store.dispatch(fetchUserById(3))

export default slice.reducer;