import { combineSlices, configureStore } from "@reduxjs/toolkit";
import { LocationSlice } from "../app/LocationSlice";
import { api1, api2 } from "../app/api";
import { SortTypeSlice } from "./SortTypeSlice";
import { SearchInputSlice } from "./SearchInputSlice";
import { persistReducer, persistStore } from "redux-persist";
import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "root",
  storage: storage,
  whitelist: ["location"],
};

const rootReducer = combineSlices(
  SearchInputSlice,
  LocationSlice,
  SortTypeSlice,
  {
    [api1.reducerPath]: api1.reducer,
    [api2.reducerPath]: api2.reducer,
  }
);

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ serializableCheck: false })
      .concat(api1.middleware)
      .concat(api2.middleware),
});

export const persistor = persistStore(store);
