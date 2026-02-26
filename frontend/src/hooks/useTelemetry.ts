import { useState, useEffect } from 'react';
import type { TelemetryData } from '../types/telemetry.types';
import { wsService } from '../services/websocket-service';
import { api } from '../services/api-client';

export function useTelemetry(maxHistory: number = 100) {
  const [telemetryHistory, setTelemetryHistory] = useState<TelemetryData[]>([]);
  const [latestData, setLatestData] = useState<TelemetryData | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect WebSocket
    wsService.connect();
    setIsConnected(true);

    // Subscribe to new data
    const unsubscribe = wsService.subscribe((data: TelemetryData) => {
      setLatestData(data);
      setTelemetryHistory(prev => {
        const updated = [...prev, data];
        return updated.slice(-maxHistory); // Keep only last N records
      });
    });

    // Load initial historical data
    api.getLatestTelemetry(20).then(data => {
      setTelemetryHistory(data);
      if (data.length > 0) {
        setLatestData(data[data.length - 1]);
      }
    });

    return () => {
      unsubscribe();
      wsService.disconnect();
      setIsConnected(false);
    };
  }, [maxHistory]);

  return { telemetryHistory, latestData, isConnected };
}