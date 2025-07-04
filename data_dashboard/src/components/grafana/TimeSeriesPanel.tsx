import "./TimeSeriesPanel.css";
import { FaRegQuestionCircle } from "react-icons/fa";
import { useState } from "react";
import getUnixTimeStamp from "../../utils/getUnixTimeStamp";
import Modal from "../modal/Modal";
import HelpContent from "../modal/HelpContent";

const TimeSeriesPanel = ({ location_id }: { location_id: string }) => {
  const [metric, setMetric] = useState("temperature");
  const [isModalOpen, setIsModalOpen] = useState(false);

  const now = new Date();
  const pad = (num: number) => num.toString().padStart(2, "0");

  const endDate = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(
    now.getDate()
  )}`;
  const startDate = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(
    now.getDate()
  )}`;

  const [dates, setDates] = useState({
    startDate: startDate,
    endDate: endDate,
  });

  const metricChangeHandler = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setMetric(e.target.value);
    console.log(src);
  };

  const dateChangeHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setDates((prev) => {
      let newDates = { ...prev, [name]: value };

      if (name === "startDate" && value > prev.endDate) {
        newDates.endDate = value;
      }
      if (name === "endDate" && value < prev.startDate) {
        newDates.startDate = value;
      }

      return newDates;
    });
  };

  const from = getUnixTimeStamp(dates.startDate);
  const to = getUnixTimeStamp(dates.endDate);

  const src = `${
    import.meta.env.VITE_GRAFANA_HOST_IP
  }&from=${from}&to=${to}&timezone=browser&var-location_id=${location_id}&var-metric=${metric}&theme=light&panelId=1&__feature.dashboardSceneSolo`;

  return (
    <div className="time_series_panel_main_frame">
      <div className="time_series_panel_title">상세 데이터 조회</div>
      <div className="time_series_panel_header_wrapper">
        <div className="time_series_panel_select_item_frame">
          <div className="time_series_panel_select_item">
            <div>조회 항목: </div>
            <select value={metric} onChange={metricChangeHandler}>
              <option value="temperature">온도</option>
              <option value="humidity">습도</option>
              <option value="tvoc">TVOC</option>
              <option value="pm10">미세먼지</option>
              <option value="pm2_5">초 미세먼지</option>
              <option value="noise">소음</option>
            </select>
          </div>
          <div className="time_series_panel_select_time">
            <div>조회 기간</div>
            <div className="time_series_panel_select_time_item">
              <div>from: </div>
              <input
                type="date"
                name="startDate"
                max={dates.endDate}
                value={dates.startDate}
                onChange={dateChangeHandler}
              />
            </div>
            <div className="time_series_panel_select_time_item">
              <div>to: </div>
              <input
                type="date"
                name="endDate"
                min={dates.startDate}
                value={dates.endDate}
                onChange={dateChangeHandler}
              />
            </div>
          </div>
        </div>
        <button
          className="time_series_panel_help_button"
          title="도움말"
          onClick={() => setIsModalOpen(true)}
        >
          <FaRegQuestionCircle />
        </button>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="도움말"
      >
        <HelpContent />
      </Modal>
      <iframe
        src={src}
        width="100%"
        height="400"
        style={{
          border: "none",
          overflow: "hidden",
        }}
        className="time_series_panel_iframe"
      ></iframe>
    </div>
  );
};

export default TimeSeriesPanel;
