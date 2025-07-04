export interface StatisticsItem {
  min: number;
  max: number;
  mean: number;
}

export interface StatisticsResponse {
  temperature: StatisticsItem;
  humidity: StatisticsItem;
  tvoc: StatisticsItem;
  noise: StatisticsItem;
  pm10: StatisticsItem;
  pm2_5: StatisticsItem;
  unit_temperature: string;
  unit_humidity: string;
  unit_tvoc: string;
  unit_noise: string;
  unit_pm: string;
  location_id: number;
  lookback_days: number;
}
