import type { Metric } from "../../../interface/Metric";
import type { PredictionItem } from "../../../interface/PredictionResponse";
import type { StatisticsResponse } from "../../../interface/StatisticsResponse";

type PredictStoryCardProps = {
  predictions: PredictionItem[];
  statistics: StatisticsResponse;
  selectedMetric: Metric;
};

const getUnitFromStatistics = (
  metric: Metric,
  statistics: StatisticsResponse
) => {
  if (metric === "temperature") return statistics.unit_temperature;
  if (metric === "humidity") return statistics.unit_humidity;
  if (metric === "tvoc") return statistics.unit_tvoc;
  if (metric === "noise") return statistics.unit_noise;
  if (metric === "pm10" || metric === "pm2_5") return statistics.unit_pm;
  return "";
};

const PredictStoryCard = ({
  predictions,
  statistics,
  selectedMetric,
}: PredictStoryCardProps) => {
  const unit = getUnitFromStatistics(selectedMetric, statistics);

  const metricName = {
    temperature: "온도",
    humidity: "습도",
    tvoc: "총 휘발성 유기화합물 농도",
    noise: "소음",
    pm10: "미세먼지 농도",
    pm2_5: "초미세먼지 농도",
  }[selectedMetric];

  // 예측 데이터에서 선택한 metric 값만 뽑아서
  const values = predictions.map((item) => item[selectedMetric]);

  const todayMax = Math.max(...values);
  const todayMin = Math.min(...values);
  const todayMean =
    values.reduce((sum, val) => sum + val, 0) / (values.length || 1);

  return (
    <div className="predict_story_card">
      <div>
        오늘의 실내 {metricName}는 최고 {todayMax.toFixed(1)}
        {unit}, 최저 {todayMin.toFixed(1)}
        {unit}, 평균 {todayMean.toFixed(1)}
        {unit}로 예상됩니다.
      </div>
      <div>
        지난 일주일 간 최고 {metricName}은{" "}
        {statistics[selectedMetric].max.toFixed(1)}
        {unit}, 최저 {statistics[selectedMetric].min.toFixed(1)}
        {unit}, 평균 {statistics[selectedMetric].mean.toFixed(1)}
        {unit}였습니다.
      </div>
    </div>
  );
};

export default PredictStoryCard;
