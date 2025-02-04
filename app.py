import fastapi
import uvicorn
from db import get_users,save_user_data,get_user_data
from ai import llm_user_response

app = fastapi.FastAPI()

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
    data = get_user_data(user_id)
    llm_response = llm_user_response(data)
    return llm_response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)