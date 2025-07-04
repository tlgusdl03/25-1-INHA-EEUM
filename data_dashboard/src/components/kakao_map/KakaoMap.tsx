import "./KakaoMap.css";
import { Map, MapMarker } from "react-kakao-maps-sdk";
import { useDispatch, useSelector } from "react-redux";
import { selectLocation, setSelectedLocation } from "../../app/LocationSlice";
import { useNavigate } from "react-router";
import parsingCoordinates from "../../utils/parsingCoordinates";
import type { Location } from "../../interface/Location";
import type { KaKaoMapProps } from "../../interface/KaKaoMapProps";

const KakaoMap = ({ data, isLoading, error }: KaKaoMapProps) => {
  // const { data, isLoading, error } = useGetLocationsQuery();
  const dispatch = useDispatch();
  const nav = useNavigate();
  const selectedLocation = useSelector(selectLocation);

  const center = selectedLocation
    ? parsingCoordinates(selectedLocation.coordinates)
    : {
        lat: 37.4493503367436,
        lng: 126.654315377117,
      };

  console.log("Selected Location:", selectedLocation);
  console.log("Center Coordinates:", center);
  console.log("Is using default center:", !selectedLocation);

  const markerClickHandler = (location: Location) => {
    try {
      if (location.location_id == selectedLocation?.location_id) {
        nav(`/${location.location_id}`);
      }
      dispatch(setSelectedLocation(location));
    } catch (error) {
      console.error("Error handling marker click:", error);
    }
  };

  if (isLoading) return <div>로딩 중...</div>;
  if (error) return <div>에러 발생</div>;

  const locations = Array.isArray(data) ? data : [data];

  return (
    <div className="kakaomap_main_frame">
      <Map
        center={center}
        style={{ width: "100%", height: "100%", minHeight: "200px" }}
      >
        {locations.map((location) => (
          <MapMarker
            key={location.location_id}
            position={parsingCoordinates(location.coordinates)}
            onClick={() => markerClickHandler(location)}
          >
            {selectedLocation?.location_id === location.location_id ? (
              <div className="kakaomap_additional_info_wrapper">
                {location.name}
              </div>
            ) : null}
          </MapMarker>
        ))}
      </Map>
    </div>
  );
};

export default KakaoMap;
