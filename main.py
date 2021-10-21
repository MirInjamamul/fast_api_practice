from typing import Optional

import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def hello_world():
    return {"Hello": "world"}

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port= 8090 )





