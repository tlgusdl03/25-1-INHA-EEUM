import Report from "./Report";
import Pattern from "./Pattern";
import Prediction from "./Prediction";
import { selectLocation } from "../../app/LocationSlice";
import { useSelector } from "react-redux";

const StatisticsInfoCard = () => {
  const location = useSelector(selectLocation);

  if (!location) {
    return <div>No location selected</div>;
  }

  return (
    <div className="statistics_info_card_main_frame">
      <Pattern />
      <Prediction />
      <Report />
    </div>
  );
};

export default StatisticsInfoCard;
