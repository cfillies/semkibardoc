import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../../setup/redux/Store'

// Define a type for the slice state
interface TotalPagesState {
  value: number
}

// Define the initial state using that type
const initialState: TotalPagesState = {
  value: 1
}

export const slice = createSlice({
  name: 'totalPages',
  initialState,
  reducers: {
    setTotalPagesNumber: (state, action: PayloadAction<{docsNumber:number, pageSize:number}>) => {
      state.value = Math.floor(action.payload.docsNumber / action.payload.pageSize) + 1;
    },
  },
});

export const { setTotalPagesNumber } = slice.actions;

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
export const totalPages = (state: RootState) => state.totalPages.value;

export default slice.reducer;
