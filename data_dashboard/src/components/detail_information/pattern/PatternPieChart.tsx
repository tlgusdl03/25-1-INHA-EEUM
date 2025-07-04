import { PieChart, Pie, Cell, Tooltip } from "recharts";
import { COLORS } from "../../../utils/patternColor";

type PatternPieChartProps = {
  data: any[]; // 나중에 정확한 타입 지정 가능
};

// 커스텀 Tooltip
const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const value = payload[0].value;
    return (
      <div
        style={{
          backgroundColor: "#fff",
          border: "1px solid #ccc",
          padding: "5px",
          fontSize: "14px",
        }}
      >
        {`${Math.round(value * 100)}%`}
      </div>
    );
  }
  return null;
};

const PatternPieChart = ({ data }: PatternPieChartProps) => {
  if (!data || data.length === 0) return null;

  return (
    <PieChart width={200} height={200}>
      <Pie
        data={data}
        cx="50%"
        cy="50%"
        innerRadius={60}
        outerRadius={80}
        dataKey="ratio"
      >
        {data.map((_, i) => (
          <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />
        ))}
      </Pie>
      <Tooltip content={<CustomTooltip />} />
    </PieChart>
  );
};

export default PatternPieChart;
