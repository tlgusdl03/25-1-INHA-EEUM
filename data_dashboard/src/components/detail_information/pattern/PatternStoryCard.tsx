import type { Metric } from "../../../interface/Metric";
import { COLORS } from "../../../utils/patternColor";

type PatternStoryCardProps = {
  item: any;
  metric: Metric;
  index: number;
};

const pattern_standard: Record<Metric, Record<string, string>> = {
  temperature: {
    EXTREME: "실내 온도가 매우 높습니다",
    VERY_HIGH: "실내가 더운 편입니다",
    HIGH: "실내가 약간 덥습니다",
    MODERATE: "실내 온도가 쾌적합니다",
    STABLE: "실내가 선선합니다",
    VERY_STABLE: "실내가 다소 쌀쌀합니다",
    LOW: "실내가 춥습니다",
  },
  humidity: {
    EXTREME: "습도가 매우 높아 불쾌할 수 있습니다",
    VERY_HIGH: "습도가 높아 다소 답답할 수 있습니다",
    HIGH: "습도가 약간 높습니다",
    MODERATE: "습도가 쾌적한 수준입니다",
    STABLE: "습도가 쾌적합니다",
    VERY_STABLE: "습도가 약간 낮습니다",
    LOW: "실내가 매우 건조합니다",
  },
  noise: {
    EXTREME: "실내 소음이 매우 높습니다",
    VERY_HIGH: "실내 소음이 높습니다",
    HIGH: "실내 소음이 다소 높습니다",
    MODERATE: "실내 소음이 보통 수준입니다",
    STABLE: "실내가 조용한 편입니다",
    VERY_STABLE: "실내가 매우 조용합니다",
    LOW: "실내가 아주 고요합니다",
  },
  tvoc: {
    EXTREME: "휘발성 유기화합물 농도가 매우 높습니다",
    VERY_HIGH: "공기질이 나쁩니다",
    HIGH: "공기질이 다소 나쁩니다",
    MODERATE: "공기질이 보통입니다",
    STABLE: "공기질이 좋습니다",
    VERY_STABLE: "공기가 매우 깨끗합니다",
  },
  pm10: {
    EXTREME: "미세먼지 농도가 매우 높습니다",
    VERY_HIGH: "미세먼지 농도가 높습니다",
    HIGH: "미세먼지 농도가 다소 높습니다",
    MODERATE: "미세먼지 농도가 보통입니다",
    STABLE: "미세먼지 농도가 낮습니다",
    VERY_STABLE: "미세먼지 농도가 매우 낮습니다",
  },
  pm2_5: {
    EXTREME: "초미세먼지 농도가 매우 높습니다",
    VERY_HIGH: "초미세먼지 농도가 높습니다",
    HIGH: "초미세먼지 농도가 다소 높습니다",
    MODERATE: "초미세먼지 농도가 보통입니다",
    STABLE: "초미세먼지 농도가 낮습니다",
    VERY_STABLE: "초미세먼지 농도가 매우 낮습니다",
  },
};

const getTimeRangeSentence = (ratio: number, start: string, end: string) => {
  const formatTime = (time: string) => {
    const [hourStr, minuteStr] = time.split(":");
    const hour = Number(hourStr);
    const minute = Number(minuteStr);

    if (hour === 0 && minute === 0) {
      return "자정";
    } else if (hour === 12 && minute === 0) {
      return "정오";
    } else if (hour < 12) {
      return `오전 ${hour}시`;
    } else {
      return `오후 ${hour === 12 ? 12 : hour - 12}시`;
    }
  };

  return `전체 기간 중 ${Number(ratio * 100).toFixed(
    0
  )}% 기간 동안, 주로 ${formatTime(start)}에서 ${formatTime(end)} 사이`;
};

const getRecommendation = (metric: Metric, pattern: string) => {
  if (metric === "temperature") {
    if (["EXTREME", "VERY_HIGH", "HIGH"].includes(pattern)) {
      return "환기 또는 냉방이 필요할 수 있습니다.";
    } else if (["STABLE", "VERY_STABLE", "LOW"].includes(pattern)) {
      return "난방 또는 창문을 닫는 것이 좋습니다.";
    } else {
      return "쾌적한 상태입니다.";
    }
  }
  if (metric === "humidity") {
    if (["EXTREME", "VERY_HIGH", "HIGH"].includes(pattern)) {
      return "제습기를 사용하는 것이 좋습니다.";
    } else if (["STABLE", "VERY_STABLE", "LOW"].includes(pattern)) {
      return "가습기를 사용하는 것이 좋습니다.";
    } else {
      return "쾌적한 습도입니다.";
    }
  }
  if (metric === "noise") {
    if (["EXTREME", "VERY_HIGH", "HIGH"].includes(pattern)) {
      return "소음 차단이 필요할 수 있습니다.";
    } else {
      return "조용한 상태입니다.";
    }
  }
  if (metric === "tvoc") {
    if (["EXTREME", "VERY_HIGH", "HIGH"].includes(pattern)) {
      return "환기를 추천합니다.";
    } else {
      return "공기가 깨끗한 상태입니다.";
    }
  }
  if (metric === "pm10" || metric === "pm2_5") {
    if (["EXTREME", "VERY_HIGH", "HIGH"].includes(pattern)) {
      return "공기청정기를 사용하는 것이 좋습니다.";
    } else {
      return "미세먼지 농도가 양호합니다.";
    }
  }
  return "";
};

const getUnit = (metric: Metric) => {
  if (metric === "temperature") return "°C";
  if (metric === "humidity") return "%";
  if (metric === "noise") return "dB";
  if (metric === "tvoc") return "ppb";
  if (metric === "pm10" || metric === "pm2_5") return "㎍/㎥";
  return "";
};

export const PatternStoryCard = ({
  item,
  metric,
  index,
}: PatternStoryCardProps) => {
  const timeSentence = getTimeRangeSentence(
    item.ratio,
    item.peak_time.start,
    item.peak_time.end
  );
  const unit = getUnit(metric);
  const valueSentence = `${item.center_value.toFixed(2)}${unit}`;
  const patternDescription = pattern_standard[metric][item.pattern];
  const recommendation = getRecommendation(metric, item.pattern);

  const story = `${timeSentence}, 실내 ${
    metric === "temperature"
      ? "온도"
      : metric === "humidity"
      ? "습도"
      : metric === "noise"
      ? "소음"
      : metric === "tvoc"
      ? "TVOC"
      : metric === "pm10"
      ? "미세먼지"
      : metric === "pm2_5"
      ? "초미세먼지"
      : ""
  }가 ${valueSentence}로 ${patternDescription}. ${recommendation}`;

  return (
    <div
      style={{ display: "flex", alignItems: "center", marginBottom: "20px" }}
    >
      {/* 네모 박스 */}
      <div
        className="pattern_story_card_box"
        style={{
          width: "0.75rem",
          height: "0.75rem",
          backgroundColor: COLORS[index % COLORS.length],
          marginRight: "0.5rem",
          borderRadius: "0.125rem",
        }}
      />
      {/* 스토리 텍스트 */}
      <div className="pattern_story_card_text">{story}</div>
    </div>
  );
};
