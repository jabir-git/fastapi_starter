import asyncio
from pathlib import Path

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from watchfiles import awatch

router = APIRouter()

# Track active WebSocket connections
websocket_connections = set()

# Track if the file watcher has been started
watcher_started = False

# Folders to watch for changes (use absolute paths)
script_dir = Path(__file__).parent.resolve()
watch_paths = [script_dir / "templates", script_dir / "static"]


async def watch_files():
    """Watch files in templates and static directories and send reload signal on changes."""
    async for changes in awatch(*watch_paths):
        # Send reload signal to all connected clients
        disconnected = set()
        for websocket in websocket_connections:
            try:
                await websocket.send_text("reload")
                print("Application is reloading...")
            except Exception:
                disconnected.add(websocket)

        # Remove disconnected clients
        for ws in disconnected:
            websocket_connections.discard(ws)


@router.websocket("/reload")
async def reload(websocket: WebSocket):
    global watcher_started

    # Accept the WebSocket connection
    await websocket.accept()

    # Add this connection to the set
    websocket_connections.add(websocket)

    # Start the file watcher on first connection
    if not watcher_started:
        watcher_started = True
        asyncio.create_task(watch_files())

    try:
        # Keep the connection alive
        while True:
            try:
                await websocket.receive_text()
            except WebSocketDisconnect:
                break
            except Exception:
                break
    finally:
        # Remove this connection from the set when it closes
        websocket_connections.discard(websocket)
