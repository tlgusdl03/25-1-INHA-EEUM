import type { Location } from "./Location";

export interface KaKaoMapProps {
  data: Location[] | Location;
  isLoading: boolean;
  error: any;
}
