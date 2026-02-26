export interface Position {
  latitude: number;
  longitude: number;
  altitude?: number;
  normalized_x?: number;
  normalized_y?: number;
}

export interface Motion {
  speed?: number;
  acceleration_x?: number;
  acceleration_y?: number;
  acceleration_z?: number;
  heading?: number;
}

export interface Sensors {
  temperature_engine?: number;
  temperature_ambient?: number;
}

export interface TelemetryData {
  timestamp: string;
  device_id: string;
  position: Position;
  motion?: Motion;
  sensors?: Sensors;
}

export interface TrackInfo {
  name: string;
  location: string;
  length_km: number;
  turns: number;
  center: {
    latitude: number;
    longitude: number;
  };
  dimensions: {
    width_meters: number;
    height_meters: number;
  };
  notable_corners?: {
    turn: number;
    name: string;
  }[];
}