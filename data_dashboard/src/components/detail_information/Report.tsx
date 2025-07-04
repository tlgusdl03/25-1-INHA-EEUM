import { useSelector } from "react-redux";
import "./Report.css";
import { selectLocation } from "../../app/LocationSlice";
import { useGetReportByIdQuery } from "../../app/api";

const Report = () => {
  const location = useSelector(selectLocation);

  if (!location) {
    return <div>No location selected</div>;
  }

  const { data: report } = useGetReportByIdQuery(location.location_id, {
    skip: !location,
  });

  return (
    <div className="report_main_frame">
      <div className="report_title_frame">요약 리포트</div>
      <div className="report_content_frame">
        <div className="report_content_text_frame">
          {report?.content
            .replace(/\\n/g, "\n")
            .split("\n")
            .map((line, idx) => (
              <div key={idx} className="report_content_text_line">
                {line}
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default Report;
