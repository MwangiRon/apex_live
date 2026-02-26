
import type { WebSocketMessage } from '../types/session.types';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/telemetry';

type MessageHandler = (data: any) => void;

export class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000;
  
  private telemetryListeners: MessageHandler[] = [];
  private flagListeners: MessageHandler[] = [];
  private sessionListeners: MessageHandler[] = [];
  private connectionListeners: MessageHandler[] = [];

  connect() {
    try {
      this.ws = new WebSocket(WS_URL);

      this.ws.onopen = () => {
        console.log('[WebSocket] Connected to server');
        this.reconnectAttempts = 0;
        
        // Send periodic pings
        setInterval(() => {
          if (this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send('ping');
          }
        }, 30000);
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.routeMessage(message);
        } catch (error) {
          console.error('[WebSocket] Failed to parse message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('[WebSocket] Connection error:', error);
      };

      this.ws.onclose = () => {
        console.log('[WebSocket] Connection closed');
        this.attemptReconnect();
      };
    } catch (error) {
      console.error('[WebSocket] Failed to create connection:', error);
      this.attemptReconnect();
    }
  }

  private routeMessage(message: WebSocketMessage) {
    switch (message.type) {
      case 'telemetry':
        this.telemetryListeners.forEach(listener => listener(message.data));
        break;
      case 'flag_change':
        this.flagListeners.forEach(listener => listener(message.data));
        break;
      case 'session_update':
        this.sessionListeners.forEach(listener => listener(message.data));
        break;
      case 'connection':
        this.connectionListeners.forEach(listener => listener(message.data));
        break;
      default:
        console.warn('[WebSocket] Unknown message type:', message.type);
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`[WebSocket] Reconnecting... Attempt ${this.reconnectAttempts}`);
      setTimeout(() => this.connect(), this.reconnectDelay);
    }
  }

  subscribeTelemetry(callback: MessageHandler) {
    this.telemetryListeners.push(callback);
    return () => {
      this.telemetryListeners = this.telemetryListeners.filter(l => l !== callback);
    };
  }

  subscribeFlags(callback: MessageHandler) {
    this.flagListeners.push(callback);
    return () => {
      this.flagListeners = this.flagListeners.filter(l => l !== callback);
    };
  }

  subscribeSession(callback: MessageHandler) {
    this.sessionListeners.push(callback);
    return () => {
      this.sessionListeners = this.sessionListeners.filter(l => l !== callback);
    };
  }

  subscribeConnection(callback: MessageHandler) {
    this.connectionListeners.push(callback);
    return () => {
      this.connectionListeners = this.connectionListeners.filter(l => l !== callback);
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  requestSessionState() {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send('get_session');
    }
  }
}

export const wsService = new WebSocketService();