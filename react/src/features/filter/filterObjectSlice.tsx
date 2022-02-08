import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../../setup/redux/Store'
import { AsideMenuItemFetchInterface, FilterInterface, SearchInterface } from '../../utils/interfaces'

// Define a type for the slice state

interface filterConfigurationInterface {
    filterConfiguration: FilterInterface,
    onChangeState: boolean,
    changeType: 'filtering' | 'searching' | 'newPage' | 'asideItem' |'none',
    searchConfig: SearchInterface,
    asideItemConfig: AsideMenuItemFetchInterface
  }

// Define the initial state using that type
const initialState: filterConfigurationInterface = {
    filterConfiguration:
    {
        "Antrag": true,
        "Eigangsbestätigung": true,
        "Genehmigung": true,
        "Versagung": true,
        "Stellungnahme": true,
        "Anhorungrag": true,
        "from": 0,
        "size": 5
    }, 
    onChangeState: true,
    changeType: 'filtering',
    searchConfig: {
      search: '',
      field: 'all'
    },
    asideItemConfig: {
      fieldName: '', 
      valueField: ''
    }
  }


export const slice = createSlice({
  name: 'filterObject',
  initialState,
  reducers: {
    setNewFilter: (state, action: PayloadAction<{updateFilterObject:FilterInterface}>) => {
      state.filterConfiguration = {...action.payload.updateFilterObject}
    },
    changeState: state => {state.onChangeState = !state.onChangeState},
    updateChangeType: (state, action: PayloadAction<{newChange:'filtering' | 'searching' | 'newPage' | 'asideItem' | 'none'}>) => {
      state.changeType = action.payload.newChange 
    },
    setSearchConfiguration: (state, action: PayloadAction<{updateSearchConfig:SearchInterface}>) => {
      state.searchConfig.search = action.payload.updateSearchConfig.search
      if (action.payload.updateSearchConfig.field === 'Überall' || action.payload.updateSearchConfig.field === 'Fulltext') {
        state.searchConfig.field = 'all'
      }
      if (action.payload.updateSearchConfig.field === 'Hida Text' || action.payload.updateSearchConfig.field === 'ObjNr') {
        state.searchConfig.field = 'hidas'
      }
      if (action.payload.updateSearchConfig.field === 'Addresse') {
        state.searchConfig.field = 'adresse'
      }
      // state.searchConfig = {...action.payload.updateSearchConfig}
    },
    setAsideItemConfiguration: (state, action: PayloadAction<{updateAsideItemConfig:AsideMenuItemFetchInterface}>) => {
      state.asideItemConfig = {...action.payload.updateAsideItemConfig}
    },
  },
});

export const { setNewFilter } = slice.actions;
export const { changeState } = slice.actions;
export const { updateChangeType } = slice.actions;
export const { setSearchConfiguration } = slice.actions;
export const { setAsideItemConfiguration } = slice.actions;

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
export const newFilter = (state: RootState) => state.updateFilter.filterConfiguration;
export const currentState = (state: RootState) => state.updateFilter.onChangeState;
export const currentChangeType = (state: RootState) => state.updateFilter.changeType;
export const searchConfigurations = (state: RootState) => state.updateFilter.searchConfig;
export const asideItemConfigurations = (state: RootState) => state.updateFilter.asideItemConfig;

export default slice.reducer;
