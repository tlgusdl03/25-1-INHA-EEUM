import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

const initialState = {
  sortType: "total_score",
  sortOrder: "desc",
};

export const SortTypeSlice = createSlice({
  name: "sortType",
  initialState: initialState,
  reducers: {
    setSortType: (state, action: PayloadAction<string>) => {
      state.sortType = action.payload;
    },
    setSortOrder: (state, action: PayloadAction<string>) => {
      state.sortOrder = action.payload;
    },
  },
  selectors: {
    selectSortType: (state) => state.sortType,
    selectSortOrder: (state) => state.sortOrder,
  },
});

export const { setSortType, setSortOrder } = SortTypeSlice.actions;
export const { selectSortType, selectSortOrder } = SortTypeSlice.selectors;
