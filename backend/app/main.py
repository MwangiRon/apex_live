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
    WebSocket endpoint for real-time telemetry streaming.
    Frontend connects here to receive live data.
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive (client can send ping messages)
            data = await websocket.receive_text()
            
            # Echo back for debugging
            if data == "ping":
                await websocket.send_text("pong")
    
    except WebSocketDisconnect:
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