import sqlite3
import uuid
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException

# 1. 配置存储目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 2. 定义获取临时数据库连接的函数
def get_db_connection():
    conn = sqlite3.connect('file.db')
    conn.row_factory = sqlite3.Row  # 让查询结果能转成字典
    return conn

# 3. 定义“生命周期”函数（取代旧的 on_event）
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：建表
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
    yield  # 把控制权交给 FastAPI，开始提供服务
    # 关闭时：什么都不用做

# 4. 先定义了 lifespan，再把它传给 FastAPI
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello, this is my first API!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 安全检查
    MAX_SIZE = 5 * 1024 * 1024
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="文件太大了")
    
    ALLOWED_TYPES = ["image/jpeg", "image/png", "application/pdf", "application/msword", 
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="只能上传JPG/PNG/PDF/WORD文件")

    # 安全重命名
    file_extension = file.filename.split(".")[-1] if "." in file.filename else 'txt'
    safe_filename = f"{uuid.uuid4().hex}.{file_extension}"
    save_path = os.path.join(UPLOAD_DIR, safe_filename)

    # 写入硬盘
    with open(save_path, "wb") as buffer:
        buffer.write(contents)

    # 写入数据库
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO uploaded_files (filename) VALUES (?)", (safe_filename,))
    conn.commit()
    conn.close() 

    return {
        "original_filename": file.filename,
        "saved_as": safe_filename,
        "status": "文件已保存至服务器！"
    }

@app.get("/files")
def list_files():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM uploaded_files")
    rows = cursor.fetchall()
    conn.close() 

    # 转换数据格式返回
    file_list = [dict(row) for row in rows]
    return {"total": len(file_list), "files": file_list}