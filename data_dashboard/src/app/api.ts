import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { Location } from "../interface/Location";
import type { IotDevice } from "../interface/IotDevice";
import type { SummaryReport } from "../interface/SummaryReport";
import type { Score } from "../interface/Score";
import type { Feedback } from "../interface/Feedback";
import type { WeatherResponse } from "../interface/WeatherResponse";
import type { StatisticsResponse } from "../interface/StatisticsResponse";
import type { ClusterPatternResponse } from "../interface/PatternResponse";
import type { PredictionResponse } from "../interface/PredictionResponse";

const api1BaseUrl = import.meta.env.VITE_API1_BASE_URL;
const api2BaseUrl = import.meta.env.VITE_API2_BASE_URL;

if (!api1BaseUrl || !api2BaseUrl) {
  throw new Error("API Base URL is not defined in environment variables.");
}

export const api1 = createApi({
  reducerPath: "api1",
  baseQuery: fetchBaseQuery({
    baseUrl: api1BaseUrl,
  }),

  endpoints: (builder) => ({
    getLocations: builder.query<Location[], void>({
      query: () => "locations",
    }),
    getLocationById: builder.query<Location, string>({
      query: (id) => `locations/${id}`,
    }),
    getIotDeviceStateById: builder.query<IotDevice[], string>({
      query: (id) => `iot_devices/${id}`,
    }),
    getReportById: builder.query<SummaryReport, string>({
      query: (location_id) => `reports/${location_id}`,
    }),
    getScores: builder.query<Score[], void>({
      query: () => "scores",
    }),
    getScoreById: builder.query<Score, string>({
      query: (location_id) => `scores/${location_id}`,
    }),
    submitFeedback: builder.mutation<void, Feedback>({
      query: (feedback) => ({
        url: "feedbacks",
        method: "POST",
        body: feedback,
      }),
    }),
  }),
});

export const api2 = createApi({
  reducerPath: "api2",
  baseQuery: fetchBaseQuery({
    baseUrl: api2BaseUrl,
  }),

  endpoints: (builder) => ({
    getWeatherForecast: builder.query<WeatherResponse, void>({
      query: () => "weather/forecast",
    }),
    getStatistics: builder.query<
      StatisticsResponse,
      { location_id: number; lookback_days: number }
    >({
      query: ({ location_id, lookback_days }) =>
        `statistics/all?location_id=${location_id}&lookback_days=${lookback_days}`,
    }),
    getPatterns: builder.query<
      ClusterPatternResponse,
      { location_id: number; lookback_days: number }
    >({
      query: ({ location_id, lookback_days }) =>
        `patterns?location_id=${location_id}&lookback_days=${lookback_days}`,
    }),
    getPrediction: builder.query<
      PredictionResponse,
      { location_id: number; lookback_days: number }
    >({
      query: ({ location_id, lookback_days }) =>
        `prediction?location_id=${location_id}&lookback_days=${lookback_days}`,
    }),
  }),
});

export const {
  useGetLocationsQuery,
  useGetLocationByIdQuery,
  useGetIotDeviceStateByIdQuery,
  useGetReportByIdQuery,
  useGetScoresQuery,
  useGetScoreByIdQuery,
  useSubmitFeedbackMutation,
} = api1;

export const {
  useGetWeatherForecastQuery,
  useGetStatisticsQuery,
  useGetPatternsQuery,
  useGetPredictionQuery,
} = api2;
