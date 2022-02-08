import {configureStore, getDefaultMiddleware} from '@reduxjs/toolkit'
import createSagaMiddleware from 'redux-saga'
import {reduxBatch} from '@manaflair/redux-batch'
import {persistStore} from 'redux-persist'

import {rootReducer, rootSaga} from './RootReducer'
import counterReducer from '../../features/filter/counterSlice'
import totalPagesReducer from '../../features/filter/totalPagesSlice'
import allFetchedDocumentsReducer from '../../features/filter/documentsSlice'
import filterObjectReducer from '../../features/filter/filterObjectSlice'

const sagaMiddleware = createSagaMiddleware()
const middleware = [
  ...getDefaultMiddleware({
    immutableCheck: false,
    serializableCheck: false,
    thunk: true,
  }),
  sagaMiddleware,
]

const store = configureStore({
  reducer: {
    rootReducer,
    counter: counterReducer,
    totalPages: totalPagesReducer,
    documentsSlice: allFetchedDocumentsReducer,
    updateFilter: filterObjectReducer
  },
  middleware,
  // middleware: getDefaultMiddleware =>
  //   getDefaultMiddleware(),
  devTools: process.env.NODE_ENV !== 'production',
  enhancers: [reduxBatch],
})

export type RootState = ReturnType<typeof store.getState>

export type AppDispatch = typeof store.dispatch

/**
 * @see https://github.com/rt2zz/redux-persist#persiststorestore-config-callback
 * @see https://github.com/rt2zz/redux-persist#persistor-object
 */
export const persistor = persistStore(store)

sagaMiddleware.run(rootSaga)

export default store
