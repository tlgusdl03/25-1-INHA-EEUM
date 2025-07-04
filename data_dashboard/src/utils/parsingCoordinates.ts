const parsingCoordinates = (
  coordinates: string
): { lat: number; lng: number } => {
  const trimed = coordinates.trim().replace(/[()]/g, "");
  const [lngStr, latStr] = trimed.split(",");
  const lng = parseFloat(lngStr.trim());
  const lat = parseFloat(latStr.trim());
  return { lat, lng };
};

export default parsingCoordinates;
