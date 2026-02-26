import { useState, useEffect } from 'react';
import { TelemetryData } from '../types/telemetry.types';
import { FlagState, SessionState } from '../types/session.types';
import { wsService } from '../services/websocket-service';
import { api } from '../services/api-client';

export function useTelemetry(maxHistory: number = 100) {
  const [telemetryHistory, setTelemetryHistory] = useState<TelemetryData[]>([]);
  const [latestData, setLatestData] = useState<TelemetryData | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [currentFlag, setCurrentFlag] = useState<FlagState | null>(null);
  const [sessionState, setSessionState] = useState<SessionState | null>(null);

  useEffect(() => {
    // Connect WebSocket
    wsService.connect();

    // Subscribe to connection status
    const unsubConnection = wsService.subscribeConnection((data) => {
      if (data.status === 'connected') {
        setIsConnected(true);
        console.log('[Telemetry] WebSocket connected');
      }
    });

    // Subscribe to telemetry data
    const unsubTelemetry = wsService.subscribeTelemetry((data: TelemetryData) => {
      setLatestData(data);
      setTelemetryHistory(prev => {
        const updated = [...prev, data];
        return updated.slice(-maxHistory);
      });
    });

    // Subscribe to flag changes
    const unsubFlags = wsService.subscribeFlags((data: FlagState) => {
      setCurrentFlag(data);
      console.log('[Telemetry] Flag changed:', data.flag_type);
    });

    // Subscribe to session updates
    const unsubSession = wsService.subscribeSession((data: SessionState) => {
      setSessionState(data);
      setCurrentFlag(data.current_flag);
      console.log('[Telemetry] Session updated');
    });

    // Load initial historical data
    api.getLatestTelemetry(20).then(data => {
      setTelemetryHistory(data);
      if (data.length > 0) {
        setLatestData(data[data.length - 1]);
      }
    }).catch(err => {
      console.error('[Telemetry] Failed to load history:', err);
    });

    // Request current session state
    setTimeout(() => {
      wsService.requestSessionState();
    }, 1000);

    return () => {
      unsubConnection();
      unsubTelemetry();
      unsubFlags();
      unsubSession();
      wsService.disconnect();
      setIsConnected(false);
    };
  }, [maxHistory]);

  return { 
    telemetryHistory, 
    latestData, 
    isConnected, 
    currentFlag,
    sessionState 
  };
}