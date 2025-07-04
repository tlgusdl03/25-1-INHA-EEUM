import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts";

type Prediction = {
  datetime: string;
  temperature: number;
  humidity: number;
  tvoc: number;
  noise: number;
  pm10: number;
  pm2_5: number;
};

type Metric = "temperature" | "humidity" | "tvoc" | "noise" | "pm10" | "pm2_5";

type PredictLineChartProps = {
  predictions: Prediction[];
  selectedMetric: Metric;
};

const formatToKST = (utcString: string) => {
  const date = new Date(utcString);
  date.setHours(date.getHours());
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hour = String(date.getHours()).padStart(2, "0");
  return `${month}-${day} ${hour}시`;
};

const PredictLineChart = ({
  predictions,
  selectedMetric,
}: PredictLineChartProps) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={predictions}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="datetime" tickFormatter={formatToKST} minTickGap={20} />
        <YAxis domain={["auto", "auto"]} />
        <Tooltip
          labelFormatter={(label) => formatToKST(label)}
          formatter={(value: number) => value.toFixed(2)}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey={selectedMetric}
          stroke="#8884d8"
          activeDot={{ r: 8 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PredictLineChart;
