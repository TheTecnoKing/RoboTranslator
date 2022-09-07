from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware 
import json
import os
from asyncio import sleep
from pydantic import BaseModel

with open("config.json", mode="r") as config:
    settings = json.load(config)

app = FastAPI()
origins = [
    "*"
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

@app.get("/")
async def root():
    return {"message": "Connettiti al WebSocket per poter visualizzare i dati dei robot in tempo reale!"}

class Data(BaseModel):
    data: int

class Item(BaseModel):
    name: str

@app.post('/command')
async def command(data: Data):
    print(data)
    with open('./data/input0.txt', mode='wb') as f:
        f.write(b'a')
        f.write(data.data.to_bytes(2, 'little'))
        f.close()
    return 200

@app.post('/test')
async def test(item: Item):
    print(item)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        dir = os.listdir("data")
        data = []
        for f in dir:
            if f[0] != 'i':
                with open("data/" + f, mode="r") as file:
                    data.append(file.read())
                    file.close()
        await websocket.send_json(json.dumps(data))
        await sleep(settings["refreshInterval"])