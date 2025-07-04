export interface PredictionResponse {
  predictions: Prediction[];
}

interface Prediction {
  datetime: string; // ISO 8601 형식의 날짜 문자열
  temperature: number;
  humidity: number;
  tvoc: number;
  noise: number;
  pm10: number;
  pm2_5: number;
}

export type PredictionItem = {
  datetime: string;
  temperature: number;
  humidity: number;
  tvoc: number;
  noise: number;
  pm10: number;
  pm2_5: number;
};
