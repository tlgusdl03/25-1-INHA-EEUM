import type { Location } from "../interface/Location";

const filterLocationList = (locationData: Location[], searchInput: string) => {
  if (!searchInput) return locationData;

  return locationData.filter((location) => {
    return location.name.toLowerCase().includes(searchInput.toLowerCase());
  });
};

export default filterLocationList;
