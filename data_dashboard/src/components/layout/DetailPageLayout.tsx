import "./DetailPageLayout.css";
import DetailPageLeftPanel from "./DetailPageLeftPanel";
import DetailPageRightPanel from "./DetailPageRightPanel";
import DetailPageHeaderPanel from "./DetailPageHeaderPanel";

const DetailPageLayout = () => {
  return (
    <div className="detail_page_layout_main_frame">
      <div className="detail_page_layout_header_panel_wrapper">
        <DetailPageHeaderPanel />
      </div>
      <div className="detail_page_layout_content_wrapper">
        <div className="detail_page_layout_left_panel_wrapper">
          <DetailPageLeftPanel />
        </div>
        <div className="detail_page_layout_right_panel_wrapper">
          <DetailPageRightPanel />
        </div>
      </div>
    </div>
  );
};

export default DetailPageLayout;
