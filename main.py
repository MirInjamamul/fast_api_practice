from typing import Optional

import uvicorn
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

class ModelName(str, Enum):
    start = "start"
    reset = "reset"
    stop = "stop"

app = FastAPI(debug= True)

class Item(BaseModel):
    name : str
    description : str = None
    price : float
    tax : float = None

@app.post("/items/")
async def create_item(item:Item):
    item_dict = item.dict()
    if item.tax:
        total = item.price + item.tax
        item_dict.update({"Total Amount":total})

    return item_dict


# Path Parameters
@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if(model_name == ModelName.start):
        return {"model_name": model_name, "message": "System has been started"}
    elif(model_name == ModelName.reset):
        return {"model_name": model_name, "message": "System has been reset"}
    elif(model_name == ModelName.stop):
        return {"model_name": model_name, "message": "System has been stoped"}

@app.get("/files/{file_path:path}")
async def get_file(file_path:str):      # url/files/myUploadedFolder/recording.wav
    return {"file_path": file_path}

# Query Parameters
@app.get("/items/")
async def get_item(init:int = 0, limit:int = 10):
    return {"Initial Value": init, "Limit": limit}

# Optional Query Parameters
@app.get("/getitem/{item_id}")
async def read_items(item_id:str,q: str=None, short: bool=False):
    item = {"item_id":item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"description": "This is amazing"}
        )

    return item

# Multiple Path and query Parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id:int , item_id:str, q: str, short:bool=False):
    item = {"User id":user_id, "Item id":item_id}

    if q:
        item.update({"q":q})
    if not short:
        item.update({"Description": "There is no description"})

    return item

if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port= 8090 )





