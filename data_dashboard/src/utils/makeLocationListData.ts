import type { Location } from "../interface/Location";
import type { LocationCardProps } from "../interface/LocationCardProps";
import type { Score } from "../interface/Score";

const makeLocationListData = (
  locations: Location[],
  scores: Score[]
): LocationCardProps[] => {
  return locations.map((location) => {
    const score =
      scores.find((score) => score.location_id === location.location_id) ||
      null;
    // if (!score) {
    //   console.warn(
    //     `[makeLocationListData] No score found for location_id: ${location.location_id}, name: ${location.name}`
    //   );
    // }
    return {
      location,
      score,
    };
  });
};

export default makeLocationListData;
