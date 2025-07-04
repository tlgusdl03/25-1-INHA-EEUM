import "./SearchBar.css";
import { FaSearch } from "react-icons/fa";
import { FaSortAmountDown, FaSortAmountUp } from "react-icons/fa";
import { AiOutlineClose } from "react-icons/ai";
import { useDispatch, useSelector } from "react-redux";
import {
  setSortType,
  setSortOrder,
  selectSortOrder,
} from "../../app/SortTypeSlice";
import {
  selectSearchInput,
  setSearchInput,
  clearSearchInput,
} from "../../app/SearchInputSlice";

const SearchBar = () => {
  const dispatch = useDispatch();
  const sortOrder = useSelector(selectSortOrder);
  const searchInput = useSelector(selectSearchInput);

  const selectChangeHandler = (e: React.ChangeEvent<HTMLSelectElement>) => {
    dispatch(setSortType(e.target.value));
  };

  const sortOrderChangeHandler = (sortOrder: string) => {
    dispatch(setSortOrder(sortOrder));
  };

  const inputChangeHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.value.trim()) {
      dispatch(setSearchInput(e.target.value));
    } else {
      dispatch(clearSearchInput());
    }
  };

  const clearSearchInputHandler = () => {
    dispatch(clearSearchInput());
  };

  return (
    <div className="search_bar_main_frame">
      <div className="search_bar_upper_wrapper">
        <input
          id="user_input"
          type="text"
          value={searchInput}
          onChange={(e) => inputChangeHandler(e)}
        />
        {searchInput ? (
          <button
            id="user_submit"
            type="button"
            onClick={clearSearchInputHandler}
          >
            <AiOutlineClose />
          </button>
        ) : (
          <button id="user_submit" type="button">
            <FaSearch />
          </button>
        )}
      </div>
      <div className="search_bar_bottom_wrapper">
        <span>정렬 기준 :</span>
        <select onChange={selectChangeHandler}>
          <option value="total_score">종합 점수</option>
          <option value="discomfort_score">불쾌 지수</option>
          <option value="cai_score">통합 대기 환경 지수</option>
          <option value="noise_score">소음 지수</option>
        </select>
        {sortOrder === "desc" ? (
          <button onClick={() => sortOrderChangeHandler("asc")}>
            <FaSortAmountDown />
          </button>
        ) : (
          <button onClick={() => sortOrderChangeHandler("desc")}>
            <FaSortAmountUp />
          </button>
        )}
      </div>
    </div>
  );
};

export default SearchBar;
