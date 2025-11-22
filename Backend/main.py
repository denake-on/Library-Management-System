from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

# Import the books API router
from api.books import router as books_router
from api.information import router as information_router
from api.librarianReaderOperation import router as librarian_reader_operation_router
from api.librarianBookOperation import router as librarian_book_operation_router
from api.director import router as director_operation_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Library Management System API")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers
app.include_router(books_router, prefix="/api", tags=["books"])
app.include_router(information_router, prefix="/api", tags=["information"])
app.include_router(librarian_reader_operation_router, prefix="/api", tags=["librarianReaderOperation"])
app.include_router(librarian_book_operation_router, prefix="/api", tags=["librarianBookOperation"])
app.include_router(director_operation_router,prefix = "/api", tags = ["directorOperation"])

# Define request model
class LoginRequest(BaseModel):
    id: str
    password: str
    identity: str  # 'reader', 'librarian', or 'director'

def verify_credentials(identity: str, user_id: str, entered_password: str) -> tuple[bool, Optional[str]]:
    """
    根据身份和ID验证密码
    返回 (是否验证成功, 错误信息)
    """
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        if identity == 'reader':
            # 查询读者表 - 使用 student_id 字段
            cursor.execute("SELECT password FROM reader_information WHERE student_id = ?", (user_id,))
        elif identity == 'librarian':
            # 查询管理员表
            cursor.execute("SELECT password FROM librarian_information WHERE admin_id = ?", (user_id,))
        elif identity == 'director':
            cursor.execute("SELECT password FROM director_information WHERE admin_id = ?", (user_id,))
        else:
            return False, f"Unknown identity type: {identity}"

        result = cursor.fetchone()

        # 关闭数据库连接
        conn.close()

        # 如果结果存在且密码匹配，返回True
        if result and result[0] == entered_password:
            return True, None
        else:
            return False, "Invalid credentials"

    except sqlite3.Error as e:
        logger.error(f"Database error in verify_credentials: {e}")
        return False, "Database error"
    except Exception as e:
        logger.error(f"Error verifying credentials: {e}")
        return False, "Server error, please check your id and retry"

def get_user_name(identity: str, user_id: str) -> str:
    """
    从数据库获取用户姓名
    """
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        if identity == 'reader':
            # 查询读者姓名
            cursor.execute("SELECT name FROM reader_information WHERE student_id = ?", (user_id,))
        elif identity == 'librarian':
            # 查询管理员姓名
            cursor.execute("SELECT name FROM librarian_information WHERE admin_id = ?", (user_id,))
        elif identity == 'director':
            # 查询馆长姓名
            cursor.execute("SELECT name FROM librarian_information WHERE admin_id = ?", (user_id,))
        else:
            return user_id  # 如果身份未知，返回ID

        result = cursor.fetchone()
        conn.close()

        if result and result[0]:
            return result[0]
        else:
            return user_id

    except sqlite3.Error as e:
        logger.error(f"Database error in get_user_name: {e}")
        return user_id
    except Exception as e:
        logger.error(f"Error getting user name: {e}")
        return user_id

@app.post("/api/login")
async def login(request: LoginRequest):
    """
    Login endpoint that receives user credentials and identity
    """
    # 终端打印信息
    print("Received login request:")
    print(f"  Identity: {request.identity}")
    print(f"  ID: {request.id}")
    print(f"  Password: {request.password}")

    # Also log to file/appropriate logging system in production
    logger.info(f"Login attempt - Identity: {request.identity}, ID: {request.id}")

    # 调用验证函数执行SQL
    is_valid, error_msg = verify_credentials(request.identity, request.id, request.password)

    if is_valid:
        # 获取用户姓名
        user_full_name = get_user_name(request.identity, request.id)

        return {
            "status": "success",
            "message": f"Login successful for {request.identity} with ID {request.id}",
            "user_id": request.id,
            "full_name": user_full_name,  # 添加用户全名信息
            "role": request.identity,
            "token": "dummy_token_for_testing"
        }
    else:
        raise HTTPException(status_code=401, detail=error_msg or "Invalid credentials")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")