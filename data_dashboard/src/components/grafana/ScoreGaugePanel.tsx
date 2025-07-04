const ScoreGaugePanel = () => {
  "http://localhost:3000/d-solo/2bc9c8ed-1eb5-42fc-a340-b929258ae4ce/select-all?orgId=1&from=1747851178024&to=1747872778024&timezone=browser&var-location_id=1&var-metric=pm2_5&var-query0=&var-score_metric=noise_score&theme=light&panelId=2&__feature.dashboardSceneSolo";
  const src = `http://${
    import.meta.env.VITE_GRAFANA_HOST_IP
  }:3000/d-solo/2bc9c8ed-1eb5-42fc-a340-b929258ae4ce/select-all?orgId=1&from=1747785775135&to=1747807375135&timezone=browser&var-query0=&var-location_id=1&panelId=1&__feature.dashboardSceneSolo`;
  return (
    <div>
      <iframe
        src={src}
        width="100%"
        height="430"
        style={{
          border: "none",
          overflow: "hidden",
        }}
      ></iframe>
    </div>
  );
};

export default ScoreGaugePanel;
