import type { Pattern } from "./Pattern";

export interface PeakTime {
  start: string; // "HH:MM" 형식
  end: string; // "HH:MM" 형식
}

export interface PatternItem {
  pattern: Pattern;
  center_value: number;
  peak_time: PeakTime;
  ratio: number;
}

export interface ClusterPatternResponse {
  temperature: PatternItem[];
  humidity: PatternItem[];
  tvoc: PatternItem[];
  noise: PatternItem[];
  pm10: PatternItem[];
  pm2_5: PatternItem[];
}
