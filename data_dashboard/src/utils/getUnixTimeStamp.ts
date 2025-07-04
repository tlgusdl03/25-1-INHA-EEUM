const getUnixTimeStamp = (dateString: string, endOfDay: boolean = false) => {
  if (!dateString) return "";

  const date = new Date(dateString);
  if (endOfDay) {
    date.setHours(23, 59, 59, 999);
  } else {
    date.setHours(0, 0, 0, 0);
  }

  return date.getTime();
};

export default getUnixTimeStamp;
