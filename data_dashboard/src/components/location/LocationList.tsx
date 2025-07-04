import "./LocationList.css";
import LocationCard from "./LocationCard";
import { useGetLocationsQuery, useGetScoresQuery } from "../../app/api";
import { useEffect, useRef } from "react";
import { selectLocation } from "../../app/LocationSlice";
import { useSelector } from "react-redux";
import makeLocationListData from "../../utils/makeLocationListData";
import { selectSortType, selectSortOrder } from "../../app/SortTypeSlice";
import sortLocationList from "../../utils/sortLocationList";
import { selectSearchInput } from "../../app/SearchInputSlice";
import filterLocationList from "../../utils/filterLocationList";

const LocationList = () => {
  const {
    data: locationData,
    isLoading: locationLoading,
    error: locationError,
  } = useGetLocationsQuery();
  const {
    data: scoreData,
    isLoading: scoreLoading,
    error: scoreError,
  } = useGetScoresQuery();

  const selectedLocation = useSelector(selectLocation);
  const sortType = useSelector(selectSortType);
  const sortOrder = useSelector(selectSortOrder);
  const cardRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const searchInput = useSelector(selectSearchInput);

  const isLoading = locationLoading || scoreLoading;
  const isError = locationError || scoreError;

  useEffect(() => {
    const ref =
      selectedLocation && cardRefs.current[selectedLocation.location_id];
    if (ref) {
      ref.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [selectedLocation]);

  if (isLoading) return <div>로딩 중...</div>;
  if (isError || !locationData || !scoreData)
    return <div>에러 또는 데이터 없음!</div>;

  const filteredData = filterLocationList(locationData, searchInput);
  const integratedData = makeLocationListData(filteredData, scoreData);
  const sortedData = sortLocationList(integratedData, sortType, sortOrder);

  return (
    <div className="location_list_main_frame">
      {sortedData.map((e) => (
        <div
          key={e.location.location_id}
          ref={(element) =>
            (cardRefs.current[e.location.location_id] = element)
          }
        >
          <LocationCard location={e.location} score={e.score} />
        </div>
      ))}
    </div>
  );
};

export default LocationList;
