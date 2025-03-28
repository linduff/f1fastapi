from fastapi import FastAPI
import requests
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

app = FastAPI()

@app.get("/openf1/{method}/{q_params}")
async def root(method: str, q_params: str):
    return getDataFromCacheOrWeb("https://api.openf1.org/v1/" + method + "?" + q_params)

@app.get("/jolpica/{path:path}")
async def root(path: str):
    return getDataFromCacheOrWeb("https://api.jolpi.ca/" + path)

def getDataFromCacheOrWeb(path):
    cached_data = r.get(path)
    if cached_data:
        print("Returning cached data")
        return json.loads(cached_data)
    else:
        print("Data not in cache. Fetching and adding to cache")
        res = requests.get(path)
        r.setex(path, 86400, json.dumps(res.json()))
        return res.json()

