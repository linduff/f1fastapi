from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def help():
    return {"text": "This API combines openf1 and jolpica in order to get all data necessary for creating an f1 webapp. Visit https://openf1.org and https://github.com/jolpica/jolpica-f1/blob/main/docs/README.md for more detail about each one. "}

@app.get("/openf1/{method}/{q_params}")
async def root(method: str, q_params: str):
    return getDataFromCacheOrWeb("https://api.openf1.org/v1/" + method + "?" + q_params)

@app.get("/jolpica/{path:path}")
async def root(path: str):
    return getDataFromCacheOrWeb("https://api.jolpi.ca/" + path)

@app.get("/healthcheck")
async def healthcheck():
    return {"healthy": True}

def getDataFromCacheOrWeb(path):
    cached_data = r.get(path)
    if cached_data:
        # print("Returning cached data")
        return json.loads(cached_data)
    else:
        # print("Data not in cache. Fetching and adding to cache")
        res = requests.get(path)
        r.setex(path, 86400, json.dumps(res.json())) # Expires after 24 hours
        return res.json()
