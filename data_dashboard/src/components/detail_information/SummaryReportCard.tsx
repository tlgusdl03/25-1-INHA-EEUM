import "./SummaryReportCard.css";
import { useGetReportByIdQuery } from "../../app/api";
import { useParams } from "react-router";

const SummaryReportCard = () => {
  const params = useParams();
  const location_id = params.location_id?.toString();

  if (!location_id) {
    return <div>Loading...</div>;
  }

  const { data, isLoading, error } = useGetReportByIdQuery(location_id, {
    skip: !location_id,
  });

  if (isLoading) return <div>로딩 중...</div>;
  if (error) return <div>에러 발생</div>;
  if (!data) return <div>데이터 없음</div>;

  console.log(data);

  return (
    <div className="summary_report_card_main_frame">
      <div className="summary_report_card_title">요약 리포트</div>
      <div className="summary_report_card_content">{data.content}</div>
    </div>
  );
};

export default SummaryReportCard;
