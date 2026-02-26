from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json
import asyncio
from fastapi.encoders import jsonable_encoder


class ConnectionManager:
    """Manages WebSocket connections for real-time telemetry and race control broadcast"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept and store new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: Dict[Any, Any], websocket: WebSocket):
        """Send message to a specific client"""
        try:
            await websocket.send_json(jsonable_encoder(message))
        except Exception as e:
            print(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[Any, Any], message_type: str = "telemetry"):
        """
        Send message to all connected clients
        
        Args:
            message: Data to broadcast
            message_type: Type of message ("telemetry", "flag_change", "session_update")
        """
        if not self.active_connections:
            return
        
        # Wrap message with type for frontend routing
        wrapped_message = {
            "type": message_type,
            "data": message,
            "timestamp": message.get("timestamp") if isinstance(message, dict) else None
        }
        
        dead_connections = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(jsonable_encoder(wrapped_message))
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                dead_connections.append(connection)
        
        # Clean up dead connections
        for connection in dead_connections:
            self.disconnect(connection)
    
    async def broadcast_telemetry(self, telemetry_data: Dict[Any, Any]):
        """Broadcast telemetry data"""
        await self.broadcast(telemetry_data, message_type="telemetry")
    
    async def broadcast_flag_change(self, flag_state: Dict[Any, Any]):
        """Broadcast flag state change"""
        await self.broadcast(flag_state, message_type="flag_change")
        print(f"Broadcasted flag change: {flag_state.get('flag_type', 'unknown')}")
    
    async def broadcast_session_update(self, session_state: Dict[Any, Any]):
        """Broadcast session state update"""
        await self.broadcast(session_state, message_type="session_update")
        print(f"Broadcasted session update")
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)


# Global connection manager instance
manager = ConnectionManager()