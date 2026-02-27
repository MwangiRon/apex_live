import type { TelemetryData, TrackInfo } from '../types/telemetry.types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface TrackWaypoint {
  name: string;
  gps: {
    latitude: number;
    longitude: number;
  };
  normalized: {
    x: number;
    y: number;
  };
}

export interface TrackLayout {
  track_name: string;
  waypoints: TrackWaypoint[];
  total_corners: number;
}

export const api = {

  async getTrackLayout(): Promise<TrackLayout> {
    const response = await fetch(`${API_URL}/api/v1/track/layout`);
    return response.json();
  },

  async getHealth() {
    const response = await fetch(`${API_URL}/api/v1/`);
    return response.json();
  },

  async getTrackInfo(): Promise<TrackInfo> {
    const response = await fetch(`${API_URL}/api/v1/track/info`);
    return response.json();
  },

  async getLatestTelemetry(limit: number = 10, deviceId?: string): Promise<TelemetryData[]> {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (deviceId) params.append('device_id', deviceId);
    
    const response = await fetch(`${API_URL}/api/v1/telemetry/latest?${params}`);
    return response.json();
  },

  async postTelemetry(data: TelemetryData): Promise<TelemetryData> {
    const response = await fetch(`${API_URL}/api/v1/telemetry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
};