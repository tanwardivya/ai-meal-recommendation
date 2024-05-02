import { configureStore } from "@reduxjs/toolkit";
import AuthReducer from "@/state";
import{
    persistReducer,
    FLUSH,
    REHYDRATE,
    PAUSE,
    PERSIST,
    PURGE,
    REGISTER
  } from "redux-persist";
import storage from 'redux-persist/lib/storage';
const persistConfig = { key: "root", storage, version: 1};
const persistedReducer = persistReducer(persistConfig, AuthReducer);
export const store = configureStore({
    reducer: persistedReducer,
    middleware:(getDefaultMiddleware) =>
      getDefaultMiddleware({
        serializableCheck: {
          ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
        },
      })
  });
export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
