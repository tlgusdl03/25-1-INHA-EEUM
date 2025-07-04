import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { SearchInputState } from "../interface/SearchInputState";

const initialState: SearchInputState = {
  searchInput: "",
};

export const SearchInputSlice = createSlice({
  name: "searchInput",
  initialState: initialState,
  reducers: {
    setSearchInput: (state, action: PayloadAction<string>) => {
      state.searchInput = action.payload;
    },
    clearSearchInput: (state) => {
      state.searchInput = "";
    },
  },
  selectors: {
    selectSearchInput: (state) => state.searchInput,
  },
});

export const { setSearchInput, clearSearchInput } = SearchInputSlice.actions;
export const { selectSearchInput } = SearchInputSlice.selectors;
