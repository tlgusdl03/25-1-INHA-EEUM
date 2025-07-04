import "./ScoreView.css";
import {
  FaRegSmile,
  FaRegMeh,
  FaRegFrown,
  FaRegAngry,
  FaRegQuestionCircle,
} from "react-icons/fa";
import type { Score } from "../../interface/Score";

const gradeToIcon = (grade: string) => {
  const gradeNumber = Number(grade);
  if (gradeNumber >= 60) {
    return <FaRegSmile className="score_view_icon score_view_icon_smile" />;
  } else if (gradeNumber >= 40) {
    return <FaRegMeh className="score_view_icon score_view_icon_meh" />;
  } else if (gradeNumber >= 20) {
    return <FaRegFrown className="score_view_icon score_view_icon_frown" />;
  } else if (gradeNumber >= 0) {
    return <FaRegAngry className="score_view_icon score_view_icon_angry" />;
  } else {
    return (
      <FaRegQuestionCircle className="score_view_icon score_view_icon_question" />
    );
  }
};

const ScoreView = ({
  score,
  sortType,
}: {
  score: Score | null;
  sortType: string | null;
}) => {
  const totalScoreIcon = gradeToIcon(score?.total_score ?? "-1");
  const discomfScoreIcon = gradeToIcon(score?.discomfort_score ?? "-1");
  const caiScoreIcon = gradeToIcon(score?.cai_score ?? "-1");
  const noiseScoreIcon = gradeToIcon(score?.noise_score ?? "-1");

  return (
    <div className="score_view_main_frame">
      <div className="score_view_main_frame_title">
        {sortType === "total_score" ? (
          <div className="score_view_main_frame_title_wrapper">
            {totalScoreIcon}
            <span>종합 지수</span>
            <span>{score?.total_score ?? "N/A"}</span>
          </div>
        ) : sortType === "discomfort_score" ? (
          <div className="score_view_main_frame_title_wrapper">
            {discomfScoreIcon}
            <span>불쾌 지수</span>
            <span>{score?.discomfort_score ?? "N/A"}</span>
          </div>
        ) : sortType === "cai_score" ? (
          <div className="score_view_main_frame_title_wrapper">
            {caiScoreIcon}
            <span>통합 대기 환경 지수</span>
            <span>{score?.cai_score ?? "N/A"}</span>
          </div>
        ) : sortType === "noise_score" ? (
          <div className="score_view_main_frame_title_wrapper">
            {noiseScoreIcon}
            <span>소음 지수</span>
            <span>{score?.noise_score ?? "N/A"}</span>
          </div>
        ) : (
          <div className="score_view_main_frame_titles_wrapper">
            <div className="score_view_main_frame_title_wrapper">
              {totalScoreIcon}
              <span>종합 지수</span>
              <span>{score?.total_score ?? "N/A"}</span>
            </div>
            <div className="score_view_main_frame_title_wrapper">
              {discomfScoreIcon}
              <span>불쾌 지수</span>
              <span>{score?.discomfort_score ?? "N/A"}</span>
            </div>
            <div className="score_view_main_frame_title_wrapper">
              {caiScoreIcon}
              <span>통합 대기 환경 지수</span>
              <span>{score?.cai_score ?? "N/A"}</span>
            </div>
            <div className="score_view_main_frame_title_wrapper">
              {noiseScoreIcon}
              <span>소음 지수</span>
              <span>{score?.noise_score ?? "N/A"}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ScoreView;
