import "./ListPageLayout.css";
import KakaoMap from "../kakao_map/KakaoMap";
import ListPanelLayout from "./ListPanelLayout";
import { useGetLocationsQuery } from "../../app/api";

const ListPageLayout = () => {
  const { data, isLoading, error } = useGetLocationsQuery();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error!</div>;
  if (!data) return <div>No data</div>;

  return (
    <div className="layout_main_frame">
      <div className="location-list">
        <ListPanelLayout />
      </div>
      <div className="kakao-map">
        <KakaoMap data={data} isLoading={isLoading} error={error} />
      </div>
    </div>
  );
};

export default ListPageLayout;
