import asyncio
import websockets
import json
import requests

API_URL = "http://localhost:8000/api/v1"
WS_URL = "ws://localhost:8000/ws/telemetry"


async def listen_to_websocket():
    """Connect to WebSocket and listen for flag changes"""
    print("Connecting to WebSocket...")
    
    async with websockets.connect(WS_URL) as websocket:
        print("Connected! Listening for messages...\n")
        
        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                
                msg_type = data.get("type")
                msg_data = data.get("data")
                
                if msg_type == "connection":
                    print(f"{msg_data.get('message')}")
                    print(f"   Active connections: {msg_data.get('active_connections')}\n")
                
                elif msg_type == "flag_change":
                    flag_type = msg_data.get("flag_type")
                    full_course = msg_data.get("full_course")
                    sectors = msg_data.get("affected_sectors", [])
                    message_text = msg_data.get("message", "")
                    
                    print("🚩" + "=" * 50)
                    print(f"   FLAG CHANGE: {flag_type.upper()}")
                    if full_course:
                        print("   Scope: FULL COURSE")
                    else:
                        print(f"   Sectors: {', '.join(sectors)}")
                    if message_text:
                        print(f"   Message: {message_text}")
                    print("=" * 53 + "\n")
                
                elif msg_type == "session_update":
                    print(f"Session Update: {msg_data.get('session_id')}")
                    print(f"   Cars: {len(msg_data.get('active_cars', []))}\n")
                
                elif msg_type == "telemetry":
                    device_id = msg_data.get("device_id")
                    speed = msg_data.get("motion", {}).get("speed", "N/A")
                    print(f"Telemetry from {device_id}: {speed} km/h")
        
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
        except KeyboardInterrupt:
            print("\n Stopping listener...")


async def trigger_flag_changes():
    """Trigger flag changes via REST API"""
    await asyncio.sleep(2)  # Wait for WebSocket to connect
    
    print("\n🎬 Starting flag change sequence...\n")
    await asyncio.sleep(2)
    
    # 1. Yellow flag in sector 2
    print("Triggering: Yellow flag in Sector 2...")
    requests.post(f"{API_URL}/flags/set", json={
        "flag_type": "yellow",
        "full_course": False,
        "sectors": ["sector_2"],
        "message": "Debris on track at Turn 4"
    })
    await asyncio.sleep(3)
    
    # 2. Double yellow (full course)
    print("Triggering: Double yellow (full course)...")
    requests.post(f"{API_URL}/flags/set", json={
        "flag_type": "double_yellow",
        "full_course": True,
        "message": "Incident ahead - no overtaking"
    })
    await asyncio.sleep(3)
    
    # 3. Red flag
    print("Triggering: Red flag...")
    requests.post(f"{API_URL}/flags/set", json={
        "flag_type": "red",
        "full_course": True,
        "message": "Session stopped"
    })
    await asyncio.sleep(3)
    
    # 4. Green flag (resume)
    print("Triggering: Green flag (racing resumed)...")
    requests.post(f"{API_URL}/flags/set", json={
        "flag_type": "green",
        "full_course": True,
        "message": "Track clear - racing resumed"
    })
    
    print("\n Flag sequence complete!")


async def main():
    """Run WebSocket listener and flag trigger in parallel"""
    # Start session first
    print("Starting race session...")
    requests.post(f"{API_URL}/session/start?session_id=test-race&session_type=race")
    print("Session started\n")
    
    # Run both tasks
    await asyncio.gather(
        listen_to_websocket(),
        trigger_flag_changes()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n Goodbye!")