import "./LocationCard.css";
import type { LocationCardProps } from "../../interface/LocationCardProps";
import { useDispatch, useSelector } from "react-redux";
import { setSelectedLocation } from "../../app/LocationSlice";
import { selectSortType } from "../../app/SortTypeSlice";
import { useNavigate } from "react-router";
import { useState } from "react";
import ScoreView from "../score/ScoreView";
const LocationCard = ({ location, score }: LocationCardProps) => {
  const dispatch = useDispatch();
  const nav = useNavigate();
  const sortType = useSelector(selectSortType);
  const [imageError, setImageError] = useState(false);

  if (!location.location_id || !location.name || !location.uri) {
    console.error("Invalid location data provided to LocationCard");
    return null;
  }

  const onClickHandler = () => {
    try {
      dispatch(setSelectedLocation(location));
      nav(`/${location.location_id}`);
    } catch (error) {
      console.error("Error handling location card click:", error);
    }
  };

  const handleImageError = () => {
    setImageError(true);
    console.error("Error loading image for location:", location.name);
  };

  return (
    <div className="location_card_main_frame" onClick={onClickHandler}>
      <div className="location_card_img_wrapper">
        {!imageError && location.uri ? (
          <img
            src={location.uri}
            alt={`${location.name} 이미지`}
            onError={handleImageError}
          />
        ) : (
          <div className="location_card_img_placeholder">
            이미지를 불러올 수 없습니다
          </div>
        )}
      </div>
      <div className="location_card_info_wrapper">
        <div className="location_name_wrapper">{location.name}</div>
        <div className="score_wrapper">
          <ScoreView score={score} sortType={sortType} />
        </div>
      </div>
    </div>
  );
};

export default LocationCard;
