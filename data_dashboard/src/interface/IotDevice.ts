export interface IotDevice {
  device_id: string,
  location_id: string,
  status: string,
  is_connected: boolean,
  last_sent_at: string,
}