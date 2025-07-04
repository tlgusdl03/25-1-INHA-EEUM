import "./HelpContent.css";

const HelpContent = () => {
  return (
    <div className="help_content_main_frame">
      <h3 className="help_content_title">데이터 조회 방법</h3>
      <p className="help_content_text">1. 조회 항목을 선택하세요.</p>
      <ul className="help_content_list">
        <li>온도: 현재 온도 데이터</li>
        <li>습도: 현재 습도 데이터</li>
        <li>TVOC: 휘발성 유기화합물 농도</li>
        <li>미세먼지: PM10 농도</li>
        <li>초미세먼지: PM2.5 농도</li>
        <li>소음: 현재 소음 레벨</li>
      </ul>
      <p className="help_content_text">2. 조회 기간을 선택하세요.</p>
      <ul className="help_content_list">
        <li>시작일: 데이터 조회 시작 날짜</li>
        <li>종료일: 데이터 조회 종료 날짜</li>
      </ul>
      <p className="help_content_text">
        ※ 종료일은 시작일보다 이후여야 합니다.
      </p>
    </div>
  );
};

export default HelpContent;
