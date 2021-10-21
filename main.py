from typing import Optional

import uvicorn
from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    start = "start"
    reset = "reset"
    stop = "stop"

app = FastAPI(debug= True)

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

if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port= 8090 )





