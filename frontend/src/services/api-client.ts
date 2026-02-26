import type { TelemetryData, TrackInfo } from '../types/telemetry.types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
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