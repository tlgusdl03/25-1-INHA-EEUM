import "./Prediction.css";
import type { Metric } from "../../interface/Metric";
import { useState } from "react";
import { useSelector } from "react-redux";
import { selectLocation } from "../../app/LocationSlice";
import { useGetPredictionQuery, useGetStatisticsQuery } from "../../app/api";
import PredictLineChart from "./predict/PredictLineChart";
import PredictStoryCard from "./predict/PredictStoryCard";

const Prediction = () => {
  const location = useSelector(selectLocation);
  const [selectedMetric, setSelectedMetric] = useState<Metric>("temperature");

  if (!location) {
    return <div>No location selected</div>;
  }

  const {
    data: prediction,
    isLoading: prediction_loading,
    error: prediction_error,
  } = useGetPredictionQuery(
    {
      location_id: Number(location.location_id),
      lookback_days: 7,
    },
    { skip: !location }
  );

  const {
    data: statistics,
    isLoading: statistics_loading,
    error: statistics_error,
  } = useGetStatisticsQuery(
    {
      location_id: Number(location.location_id),
      lookback_days: 7,
    },
    { skip: !location }
  );

  const isLoading = prediction_loading || statistics_loading;
  const error = prediction_error || statistics_error;

  return (
    <div className="prediction_main_frame">
      <div className="prediction_title_frame">오늘의 예측 결과</div>
      <div className="prediction_select_frame">
        <select
          value={selectedMetric}
          onChange={(e) => setSelectedMetric(e.target.value as Metric)}
        >
          <option value="temperature">온도</option>
          <option value="humidity">습도</option>
          <option value="tvoc">TVOC</option>
          <option value="noise">소음</option>
          <option value="pm10">미세먼지</option>
          <option value="pm2_5">초미세먼지</option>
        </select>
      </div>
      <div className="prediction_content_frame">
        {isLoading ? (
          <div className="prediction_loading_frame">
            예측 결과 불러오는 중입니다. 잠시만 기다려 주세요
          </div>
        ) : error ? (
          <div className="prediction_error_frame">
            예측 결과 불러오는 중 오류가 발생했습니다
          </div>
        ) : (
          <>
            {prediction && statistics && (
              <>
                <PredictStoryCard
                  predictions={prediction?.predictions || []}
                  statistics={statistics}
                  selectedMetric={selectedMetric}
                />
                <PredictLineChart
                  predictions={prediction?.predictions || []}
                  selectedMetric={selectedMetric}
                />
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Prediction;
