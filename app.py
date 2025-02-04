import fastapi
import uvicorn
import json

from db import get_users,save_user_data,get_user_data
from ai import llm_user_response

from redis.asyncio import Redis
from contextlib import asynccontextmanager
import httpx



import redis as sync_redis
import redis.asyncio as aioredis
from redis.asyncio import Redis


app = fastapi.FastAPI()


@app.on_event("startup")
async def startup():
    global redis_client

    # redis_client = Redis.Redis(host="localhost", port=6379, db=0)

    redis_client = Redis(host="localhost", port=6379, db=0)
    app.state.http_client = httpx.AsyncClient()
    

@app.on_event("shutdown")
async def shutdown():
    await redis_client.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
async def users():
    cols,data = get_users()
    return {"columns": cols, "data": data}

@app.post("/register_users")
async def register_users(user_access_token):
    save_user_data(user_access_token)
    return {"message": "success"}

# user id
# 642521558213634

@app.get("/llmbreif")
async def llmbreif(user_id):

    value = await redis_client.get(user_id)
    if value is None:
        data = get_user_data(user_id)
        value = llm_user_response(data)

        await redis_client.setex(user_id,time = 60 , value=value)

    return value

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)