export interface WeatherResponse {
  header: {
    resultCode: string;
    resultMsg: string;
  };
  item: WeatherItem[];
}

interface WeatherItem {
  baseDate: string;
  baseTime: string;
  fcstDate: string;
  fcstTime: string;
  category: string;
  fcstValue: string;
  nx: number;
  ny: number;
}
