import type { LocationCardProps } from "../interface/LocationCardProps";

const sortLocationList = (
  data: LocationCardProps[],
  sortType: string,
  sortOrder: string
): LocationCardProps[] => {
  if (data.length === 0) return data;

  data.sort((a, b) => {
    if (a.score && b.score) {
      if (sortType === "total_score") {
        const aScore = parseFloat(a.score.total_score);
        const bScore = parseFloat(b.score.total_score);
        return sortOrder === "asc" ? aScore - bScore : bScore - aScore;
      } else if (sortType === "cai_score") {
        const aScore = parseFloat(a.score.cai_score);
        const bScore = parseFloat(b.score.cai_score);
        return sortOrder === "asc" ? aScore - bScore : bScore - aScore;
      } else if (sortType === "noise_score") {
        const aScore = parseFloat(a.score.noise_score);
        const bScore = parseFloat(b.score.noise_score);
        return sortOrder === "asc" ? aScore - bScore : bScore - aScore;
      }
    }
    return 0;
  });
  return data;
};

export default sortLocationList;
