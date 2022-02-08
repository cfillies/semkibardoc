import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { type } from 'os';
import { string } from 'yup/lib/locale';
import type { RootState } from '../../setup/redux/Store'

interface FilterInterface {
  "Antrag": boolean,
  "Eigangsbestätigung": boolean,
  "Genehmigung": boolean,
  "Versagung": boolean,
  "Stellungnahme": boolean,
  "Anhorungrag": boolean,
  "from": number,
  "size": number
}

interface SearchInterface {
  "field": string,
  "search": string
}

interface documentsState {
  documentsList: Array<string>,

  // Multiple possible status enum values
  status: 'idle' | 'loading' | 'succeeded' | 'failed',
  error: string | null
  
}

const initialState: documentsState = {
    documentsList: [],
    status: 'idle',
    error: null
  }

export const fetchDocumentsAsync = createAsyncThunk(
    'documents/fetchDocumentsAsync', 
    async (filtersObject: FilterInterface) => {
        let request = "";
        let key: keyof FilterInterface;
        for (key in filtersObject){
            request+=key.toString();
            request+="=";
            if (key === 'from' || key === 'size'){
                request+=filtersObject[key].toString();
            }
            else {
              request+=((filtersObject[key] && "1") || "0");    
            }
            request+="&";
        }
        let req = 'http://localhost:5000/filter/?';
        req+=request.slice(0,-1);
        const response = await fetch(req);
        // console.log(response.json())
        return await (response.json()) as JSON
    }
)

export const searchDocumentsAsync = createAsyncThunk(
  'documents/searchDocumentsAsync', 
  async (filtersObject: SearchInterface) => {
    console.log("searchDocumentsAsync")
      let request = "";
      let key: keyof SearchInterface;
      for (key in filtersObject){
          request+=key.toString();
          request+="=";
          request+=filtersObject[key].toString();
          request+="&";
      }
      let req = 'http://localhost:5000/search/?';
      req+=request.slice(0,-1);
      const response = await fetch(req);
      // console.log(response.json())
      return await (response.json()) as JSON
  }
)

export const fetchItemFieldAsync = createAsyncThunk(
  'documents/fetchItemFieldAsync', 
  async (filtersObject:{fieldName: string, valueField: string}) => {
    console.log("fetchItemFieldAsync")
      
      let req = 'http://localhost:5000/asideitem/?field=' + filtersObject.fieldName + '&search=' + filtersObject.valueField;
      const response = await fetch(req);
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

export const docList = (state: RootState) => state.documentsSlice.documentsList;
export const fetchStatus = (state: RootState) => state.documentsSlice.status;
// const lastReturnedAction = await store.dispatch(fetchUserById(3))

export default slice.reducer;