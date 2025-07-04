import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import type { LocationState } from "../interface/LocationState";
import type { Location } from "../interface/Location";

const initialState: LocationState = {
  location: null,
  loading: false,
  error: null,
};

export const LocationSlice = createSlice({
  name: "location",
  initialState: initialState,
  reducers: () => ({
    setSelectedLocation: (state, action: PayloadAction<Location>) => {
      state.location = action.payload;
    },
    clearSelectedLocation: (state) => {
      state.location = null;
    },
  }),
  selectors: {
    selectLocation: (state) => state.location,
  },
});

export const { setSelectedLocation, clearSelectedLocation } =
  LocationSlice.actions;
export const { selectLocation } = LocationSlice.selectors;
