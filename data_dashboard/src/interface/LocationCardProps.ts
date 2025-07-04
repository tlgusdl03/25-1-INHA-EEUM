import type { Location } from "./Location";
import type { Score } from "./Score";

export interface LocationCardProps {
  location: Location;
  score: Score | null;
}
