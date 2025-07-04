import "./Pattern.css";
import { useSelector } from "react-redux";
import { selectLocation } from "../../app/LocationSlice";
import { useGetPatternsQuery } from "../../app/api";
import { useState } from "react";
import { PatternStoryCard } from "./pattern/PatternStoryCard";
import PatternPieChart from "./pattern/PatternPieChart";
import type { Metric } from "../../interface/Metric";

const Pattern = () => {
  const [selected_period, setSelectedPeriod] = useState<string>("weekly");
  const [selected_metric, setSelectedMetric] = useState<Metric>("temperature");
  const location = useSelector(selectLocation);

  if (!location) {
    return <div>No location selected</div>;
  }

  const {
    data: weekly_patterns,
    isLoading: weekly_patterns_loading,
    error: weekly_patterns_error,
  } = useGetPatternsQuery(
    {
      location_id: Number(location.location_id),
      lookback_days: 7,
    },
    {
      skip: !location,
    }
  );
  const {
    data: daily_patterns,
    isLoading: daily_patterns_loading,
    error: daily_patterns_error,
  } = useGetPatternsQuery(
    {
      location_id: Number(location.location_id),
      lookback_days: 1,
    },
    {
      skip: !location,
    }
  );

  const data =
    selected_period === "weekly"
      ? weekly_patterns?.[selected_metric]
      : daily_patterns?.[selected_metric];

  const isLoading =
    selected_period === "weekly"
      ? weekly_patterns_loading
      : daily_patterns_loading;

  const error =
    selected_period === "weekly" ? weekly_patterns_error : daily_patterns_error;

  return (
    <div className="pattern_main_frame">
      <div className="pattern_title_frame">패턴 분석 결과</div>
      <div className="pattern_select_frame">
        <select
          value={selected_period}
          onChange={(e) => setSelectedPeriod(e.target.value)}
        >
          <option value="weekly">주별</option>
          <option value="daily">일별</option>
        </select>
        <select
          value={selected_metric}
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
      <div className="pattern_content_frame">
        {isLoading ? (
          <div className="pattern_loading_frame">
            패턴 분석 중입니다. 잠시만 기다려 주세요
          </div>
        ) : error ? (
          <div className="pattern_error_frame">
            {selected_period === "weekly"
              ? "주별 패턴 분석 중 오류가 발생했습니다"
              : "일별 패턴 분석 중 오류가 발생했습니다"}
          </div>
        ) : (
          data && (
            <div className="pattern_content_frame">
              {data && (
                <>
                  <div className="pattern_content_frame_pie_chart">
                    <PatternPieChart data={data} />
                  </div>
                  <div className="pattern_content_frame_story_card">
                    {data.map((item, index) => (
                      <PatternStoryCard
                        key={item.pattern}
                        item={item}
                        metric={selected_metric}
                        index={index}
                      />
                    ))}
                  </div>
                </>
              )}
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default Pattern;
