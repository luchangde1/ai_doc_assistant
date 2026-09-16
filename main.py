import shutil
import uuid
import os
from fastapi import FastAPI, UploadFile, File,HTTPException

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)
@app.get("/")
def read_root():
    return {"message": "Hello, this is my first API!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    MAX_SIZE = 5 * 1024 * 1024
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400,detail="文件太大了")

    ALLOWED_TYPES = ["image/jpeg","image/png","application/pdf","application/msword","application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400,detail="只能上传JPH/PNG/PDF/WORD文件")

    file_extension = file.filename.split(".")[-1]if "." in file.filename else 'txt'
    safe_filename = f"{uuid.uuid4().hex}.{file_extension}"
    save_path = os.path.join(UPLOAD_DIR,safe_filename)

    with open(save_path,"wb")as buffer:
        buffer.write(contents)

    return{
            "original_filename":file.filename,
            "saved_as":safe_filename,
            "status":"文件已保存至服务器！"
    }
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "status": "成功收到文件！"
    }