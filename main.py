from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import websockets
import json

app = FastAPI()

todo_list = []
connected_clients = set()

async def update_clients():
    for client in connected_clients:
        await client.send_text(json.dumps({"type": "update", "data": todo_list}))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    await update_clients()

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)

            if data["type"] == "add":
                todo_list.append({"text": data["text"], "completed": False})
            elif data["type"] == "toggle":
                index = data["index"]
                todo_list[index]["completed"] = not todo_list[index]["completed"]
            elif data["type"] == "delete":
                index = data["index"]
                del todo_list[index]
            elif data["type"] == "move":
                from_index = data["fromIndex"]
                to_index = data["toIndex"]
                moved_item = todo_list.pop(from_index)
                todo_list.insert(to_index, moved_item)

            await update_clients()
    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        connected_clients.remove(websocket)


templates = Jinja2Templates(directory='.')
@app.get("/")
async def read_tasks(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
