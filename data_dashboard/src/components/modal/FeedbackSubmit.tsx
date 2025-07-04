import { useState } from "react";
import { useSubmitFeedbackMutation } from "../../app/api";

const FeedbackSubmit = ({ location_id }: { location_id: string }) => {
  const [value, setValue] = useState(50);
  const [submitFeedback, { isLoading, isSuccess }] =
    useSubmitFeedbackMutation();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(Number(e.target.value));
  };

  const handleSubmit = async () => {
    await submitFeedback({
      location_id: location_id,
      satisfaction_score: value,
    });
  };

  return (
    <div>
      <div>만족도를 알려주세요!</div>
      <input
        type="range"
        min={0}
        max={100}
        value={value}
        onChange={handleChange}
        style={{ width: "100%" }}
      />
      <div>현재 값: {value}</div>
      <button
        onClick={handleSubmit}
        disabled={isLoading}
        style={{ marginTop: "1rem" }}
      >
        {isLoading ? "제출 중..." : "제출"}
      </button>
      {isSuccess && (
        <div style={{ color: "green", marginTop: "0.5rem" }}>제출 완료!</div>
      )}
    </div>
  );
};

export default FeedbackSubmit;
