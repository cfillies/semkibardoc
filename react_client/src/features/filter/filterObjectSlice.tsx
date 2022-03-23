import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../../setup/redux/Store'
import { AsideMenuItemFetchInterface, FilterInterface, SearchInterface, AsideFiltersInterface, InnerAsideMenuInterface, AsideFiltersCounterInterface } from '../../utils/interfaces'

// Define a type for the slice state

interface filterConfigurationInterface {
    filterConfiguration: FilterInterface,
    asideFiltersConfiguration: AsideFiltersInterface,
    onChangeState: boolean,
    loadingFiltersState: boolean,
    loadingHorizontalFiltersState: boolean,
    changeType: 'filtering' | 'searching' | 'newPage' | 'asideItem'  | 'horizontalItem' |'none',
    searchConfig: SearchInterface,
    asideItemConfig: AsideMenuItemFetchInterface,
    searchState: boolean,
    docTypList: Array<InnerAsideMenuInterface>
    filterCounter: AsideFiltersCounterInterface
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
        "page": 1,
        "page_size": 10
    }, 
    asideFiltersConfiguration:
    {
      "Außenanlagen": [],
      "Baumaßnahme": [],
      "Bepflanzungen": [],
      "Brandschutz": [],
      "Dach": [],
      "Denkmalart": [],
      "Denkmalname": [],
      "Diverse": [],
      "Eingangsbereich": [],
      "Farbe": [],
      "Fassade": [],
      "Fenster": [],
      "Funk": [],
      "Gebäude": [],
      "Gebäudenutzung": [],
      "Haustechnik": [],
      "Kunst": [],
      "Maßnahme": [],
      "Nutzungsänderung": [],
      "Sachbegriff": [],
      "Solaranlage": [],
      "Treppenhaus": [],
      "Tür": [],
      "Werbeanlage": [],
      "district": [],
      "doctype": [],
      "ext": [],
      "hidas": [],
      "path": [],
      "vorhaben": []
    },
    onChangeState: true,
    loadingFiltersState: true,
    loadingHorizontalFiltersState: true,
    changeType: 'filtering',
    searchConfig: {
      search: '',
      field: 'all'
    },
    asideItemConfig: {
      fieldName: '', 
      valueField: ''
    },
    searchState: false,
    docTypList: [],
    filterCounter: {
      "Außenanlagen": 0,
      "Baumaßnahme": 0,
      "Bepflanzungen": 0,
      "Brandschutz": 0,
      "Dach": 0,
      "Denkmalart": 0,
      "Denkmalname": 0,
      "Diverse": 0,
      "Eingangsbereich": 0,
      "Farbe": 0,
      "Fassade": 0,
      "Fenster": 0,
      "Funk": 0,
      "Gebäude": 0,
      "Gebäudenutzung": 0,
      "Haustechnik": 0,
      "Kunst": 0,
      "Maßnahme": 0,
      "Nutzungsänderung": 0,
      "Sachbegriff": 0,
      "Solaranlage": 0,
      "Treppenhaus": 0,
      "Tür": 0,
      "Werbeanlage": 0,
      "district": 0,
      "doctype": 0,
      "ext": 0,
      "hidas": 0,
      "path": 0,
      "vorhaben": 0,
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
    changeLoadingFiltersState: state => {state.loadingFiltersState = !state.loadingFiltersState},
    changeLoadingHorizontalFiltersState: state => {state.loadingHorizontalFiltersState = !state.loadingHorizontalFiltersState},
    updateChangeType: (state, action: PayloadAction<{newChange:'filtering' | 'searching' | 'newPage' | 'asideItem' | 'horizontalItem' | 'none'}>) => {
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
    setAsideItemConfiguration: (state, action: PayloadAction<{updateAsideItemConfig:AsideFiltersInterface}>) => {
      state.asideFiltersConfiguration = {...action.payload.updateAsideItemConfig}
    },
    setSearchState: (state, action: PayloadAction<{searchingState:boolean}>) => {
      state.searchState = action.payload.searchingState
    },
    setDocTypList: (state, action: PayloadAction<{docTypFilterList:InnerAsideMenuInterface[]}>) => {
      state.docTypList = {...action.payload.docTypFilterList}
    },
    updateFilterCounter: (state, action: PayloadAction<{filterCounter:AsideFiltersCounterInterface}>) => {
      state.filterCounter = {...action.payload.filterCounter}
    },
  },
});

export const { setNewFilter } = slice.actions;
export const { changeState } = slice.actions;
export const { changeLoadingFiltersState } = slice.actions;
export const { changeLoadingHorizontalFiltersState } = slice.actions;
export const { updateChangeType } = slice.actions;
export const { setSearchConfiguration } = slice.actions;
export const { setAsideItemConfiguration } = slice.actions;
export const { setSearchState } = slice.actions;
export const { setDocTypList } = slice.actions;
export const { updateFilterCounter } = slice.actions;

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
export const currentLoadingFiltersState = (state: RootState) => state.updateFilter.loadingFiltersState;
export const currentChangeType = (state: RootState) => state.updateFilter.changeType;
export const searchConfigurations = (state: RootState) => state.updateFilter.searchConfig;
export const asideItemConfigurations = (state: RootState) => state.updateFilter.asideItemConfig;
export const asideFiltersConfigurations = (state: RootState) => state.updateFilter.asideFiltersConfiguration;
export const horizontalFilters = (state: RootState) => state.updateFilter.asideFiltersConfiguration.doctype;
export const currentSearchState = (state: RootState) => state.updateFilter.searchState;
export const docTypFilterList = (state: RootState) => state.updateFilter.docTypList;
export const currentDocTypFilters = (state: RootState) => state.updateFilter.loadingHorizontalFiltersState;
export const currentFilterCounter = (state: RootState) => state.updateFilter.filterCounter;

export default slice.reducer;
