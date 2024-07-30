from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
import os
import shutil
from typing import List

app = FastAPI()

# In-memory storage for clients (WebSocket connections)
clients = []

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), type: str = "unknown"):
    save_path = f"uploads/{type}"
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    await notify_clients({"type": type, "filename": file.filename})
    return {"filename": file.filename}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)

