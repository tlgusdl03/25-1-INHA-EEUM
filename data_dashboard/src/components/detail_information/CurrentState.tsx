import "./CurrentState.css";
import { FaRegSmile, FaRegFrown } from "react-icons/fa";
import { useParams } from "react-router";
import {
  useGetIotDeviceStateByIdQuery,
  useGetLocationByIdQuery,
  useGetScoreByIdQuery,
} from "../../app/api";
import ScoreView from "../score/ScoreView";
import KakaoMap from "../kakao_map/KakaoMap";

const CurrentState = () => {
  const { location_id } = useParams<{ location_id: string }>();

  const {
    data: locationData,
    isLoading: isLocationLoading,
    error: locationError,
  } = useGetLocationByIdQuery(location_id ?? "", { skip: !location_id });

  const {
    data: stateData,
    isLoading: isStateLoading,
    error: stateError,
  } = useGetIotDeviceStateByIdQuery(location_id ?? "", { skip: !location_id });

  const {
    data: scoreData,
    isLoading: isScoreLoading,
    error: scoreError,
  } = useGetScoreByIdQuery(location_id ?? "", {
    skip: !location_id,
  });

  if (isLocationLoading || isStateLoading || isScoreLoading)
    return <div>로딩 중...</div>;
  if (locationError || stateError || scoreError) return <div>에러 발생</div>;
  if (!locationData || !stateData || !scoreData) return <div>데이터 없음</div>;

  return (
    <div className="current_state_card_main_frame">
      <div className="current_state_card_location_wrapper">
        <div className="current_state_card_map_wrapper">
          <KakaoMap
            data={locationData}
            isLoading={isLocationLoading}
            error={locationError}
          />
        </div>
        <div className="current_state_card_image_wrapper">
          <img src={locationData.uri} alt="location" />
        </div>
        <div className="current_state_card_location_name">
          {locationData.name}
        </div>
      </div>
      <div className="current_state_card_status_wrapper">
        <div className="current_state_card_status_title">센서 상태</div>
        {stateData.map((state) =>
          state.status === "active" ? (
            <div key={state.device_id} className="status-container">
              <div>{`${state.device_id}번 센서`}</div>
              <FaRegSmile className="status-icon active" />
              <div>정상 작동 중</div>
            </div>
          ) : (
            <div key={state.device_id} className="status-container">
              <div>{`${state.device_id}번 센서`}</div>
              <FaRegFrown className="status-icon inactive" />
              <span>점검 중</span>
            </div>
          )
        )}
      </div>
      <div className="current_state_card_score_wrapper">
        <ScoreView score={scoreData} sortType={null} />
      </div>
    </div>
  );
};

export default CurrentState;
