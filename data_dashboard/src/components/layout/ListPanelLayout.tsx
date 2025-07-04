import LocationList from "../location/LocationList";
import SearchBar from "../search_bar/SearchBar";
import "./ListPanelLayout.css";

const ListPanelLayout = () => {
  return (
    <div className="list_panel_layout_main_frame">
      <SearchBar />
      <div className="location_list_scroll_wrapper">
        <LocationList />
      </div>
    </div>
  );
};

export default ListPanelLayout;
