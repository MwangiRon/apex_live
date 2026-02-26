from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import settings
from app.transport import api_router
from app.transport.websocket_handler import manager

# Initialize FastAPI app
app = FastAPI(
    title="F1 Telemetry API",
    description="Real-time telemetry collection and streaming for F1-style racing",
    version="1.0.0",
    debug=settings.debug
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST API routes
app.include_router(api_router)


@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    """
    WebSocket endpoint for real-time telemetry streaming and race control.
    Frontend connects here to receive:
    - Live telemetry data
    - Flag changes
    - Session updates
    """
    await manager.connect(websocket)
    
    try:
        # Send initial connection confirmation
        await manager.send_personal_message({
            "type": "connection",
            "data": {
                "status": "connected",
                "message": "WebSocket connection established",
                "active_connections": manager.get_connection_count()
            }
        }, websocket)
        
        # Send current session status if available
        from app.logic.race_controller import race_controller
        session = race_controller.get_active_session()
        if session:
            await manager.send_personal_message({
                "type": "session_update",
                "data": session.dict()
            }, websocket)
        
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            
            # Handle ping/pong
            if data == "ping":
                await websocket.send_text("pong")
            
            # Handle client requests for current state
            elif data == "get_session":
                session = race_controller.get_active_session()
                if session:
                    await manager.send_personal_message({
                        "type": "session_update",
                        "data": session.dict()
                    }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("=" * 60)
    print("F1 Telemetry API Starting...")
    print(f"Debug Mode: {settings.debug}")
    print(f"CORS Origins: {settings.cors_origins_list}")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("F1 Telemetry API Shutting Down...")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )