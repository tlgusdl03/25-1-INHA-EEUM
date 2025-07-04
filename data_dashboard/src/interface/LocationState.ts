import type { Location } from "./Location";

export interface LocationState {
  location: Location | null;
  loading: boolean;
  error: string | null;
}
