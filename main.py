from typing import Optional, List

import uvicorn
from enum import Enum
from fastapi import FastAPI , Query, Path
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

# String Validation
@app.get("/item_validate/")
async def read_items(item_id: List[str] = Query(..., max_length=10, min_length=2,title="List Of Items", description="All items in a list")):
    results = {"items": [{"item_id": "Pen"}, {"item_id": "Pencil"}]}

    if item_id:
        results.update({"item_id": item_id})

    return results

# Numeric Validation
@app.get("/item_validate/{item_id}/")
async def get_items(item_id: int = Path(..., title="Numeric Validation", gt=0 , lt=10)):
    results = {"items": [{"item_id": "Pen"}, {"item_id": "Pencil"}]}
    results.update({"New Item": item_id})

    return results

if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port= 8090 )





