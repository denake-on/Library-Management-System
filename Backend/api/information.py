from annotated_types import Len
from fastapi import APIRouter, HTTPException
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/reader-log-up")
async def register_reader(student_id: str, password: str):
    try:
        if len(student_id) != 9:
            raise HTTPException(status_code=500, detail="ID must be 9 digits")

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # 检查是否已存在相同的 student_id
        cursor.execute("SELECT 1 FROM reader_information WHERE student_id = ?", (student_id,))
        if cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=400, detail="this id already had an account")

        # 获取当前最大序号，用于生成新的 reader_id
        cursor.execute("SELECT MAX(reader_id) FROM reader_information WHERE reader_id LIKE 'reader %'")
        max_result = cursor.fetchone()[0]

        if max_result is None:
            # 如果还没有任何 reader 记录，从 1 开始
            next_number = 1
        else:
            # 从 'reader X' 格式中提取數字
            try:
                current_max_part = max_result.split(' ')[-1]  # 获取最后一个部分（数字）
                current_max = int(current_max_part)
                next_number = current_max + 1
            except (ValueError, IndexError):
                # 如果格式不正確，從1開始
                next_number = 1

        # 生成新的 reader_id
        new_reader_id = f"reader {next_number}"

        # 插入新記錄，包含生成的 reader_id
        name = "default user name, please edit it"
        cursor.execute("""
            INSERT INTO reader_information(reader_id, student_id, name, password)
            VALUES (?, ?, ?, ?)
        """, (new_reader_id, student_id, name, password))

        # 记录日志
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"Student {student_id} logged up with reader_id {new_reader_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()

        print(f"Registered new reader: {new_reader_id}, student_id: {student_id}")

        return {
            "status": "success",
            "message": "Registration successful"
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in register_reader: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error registering reader: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@router.get("/reader-information")
async def get_reader_information(student_id: str):
    """
    Get reader information by student ID
    Returns email and phone for the reader
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Query reader information by student ID
        cursor.execute("""
            SELECT student_id, name, email, phone
            FROM reader_information
            WHERE student_id = ?
        """, (student_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Reader not found")
        
        # Format the response
        reader_info = {
            "student_id": result[0],
            "name": result[1],
            "email": result[2],
            "phone": result[3]
        }
        
        # Print to backend console
        print(f"Fetched information for student {student_id}: {reader_info}")
        
        return {"information": reader_info}
        
    except sqlite3.Error as e:
        logger.error(f"Database error in get_reader_information: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error getting reader information: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/librarian-director-information")
async def get_librarian_director_information(admin_id: str, role: str):
    """
    Get librarian or director information by admin ID
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # 根据角色选择表名
        if role == 'librarian':
            table_name = 'librarian_information'
        elif role == 'director':
            table_name = 'director_information'
        else:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'librarian' or 'director'")
        
        # Query admin information by admin ID
        cursor.execute(f"""
            SELECT admin_id, name, email, phone
            FROM {table_name}
            WHERE admin_id = ?
        """, (admin_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail=f"{role.capitalize()} not found")
        
        # Format the response
        admin_info = {
            "admin_id": result[0],
            "name": result[1],
            "email": result[2] if result[2] else '',
            "phone": result[3] if result[3] else ''
        }
        
        # Print to backend console
        print(f"Fetched information for {role} {admin_id}: {admin_info}")
        
        return {"information": admin_info}
        
    except HTTPException:
        raise
    except sqlite3.Error as e:
        logger.error(f"Database error in get_librarian_director_information: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error getting {role} information: {e}")
        raise HTTPException(status_code=500, detail="Server error")

from pydantic import BaseModel
from typing import Optional

class UpdateReaderInfoRequest(BaseModel):
    student_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    

@router.post("/update-reader-information")
async def update_reader_information(request: UpdateReaderInfoRequest):
    """
    Update reader information
    """
    try:

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()


        updates = []
        params = []

        # 更新用户修正的部分
        if request.name is not None:
            updates.append("name = ?")
            params.append(request.name)

        if request.email is not None:
            updates.append("email = ?")
            params.append(request.email)

        if request.phone is not None:
            updates.append("phone = ?")
            params.append(request.phone)

        if not updates:
            conn.close()
            raise HTTPException(status_code=400, detail="No fields to update")

        # Add student_id to the end of params for WHERE clause
        params.append(request.student_id)

        query = f"UPDATE reader_information SET {', '.join(updates)} WHERE student_id = ?"
        cursor.execute(query, params)

        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Reader not found")
        
        # 记录日志
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"Student {request.student_id} updated the personal information"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()

        # Print to backend console
        update_data = {"student_id": request.student_id}
        if request.name: update_data["name"] = request.name
        if request.email: update_data["email"] = request.email
        if request.phone: update_data["phone"] = request.phone
        print(f"Updated information for student {request.student_id}: {update_data}")

        return {
            "status": "success",
            "message": "Reader information updated successfully"
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in update_reader_information: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error updating reader information: {e}")
        raise HTTPException(status_code=500, detail="Server error")

class UpdateLibrarianDirectorInfoRequest(BaseModel):
    admin_id: str
    role: str  # 'librarian' or 'director'
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    

@router.post("/update-librarian-director-information")
async def update_librarian_director_information(request: UpdateLibrarianDirectorInfoRequest):
    """
    Update librarian or director information
    """
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # 根据角色选择表名
        if request.role == 'librarian':
            table_name = 'librarian_information'
        elif request.role == 'director':
            table_name = 'director_information'
        else:
            conn.close()
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'librarian' or 'director'")

        # 检查用户是否存在
        cursor.execute(f"SELECT 1 FROM {table_name} WHERE admin_id = ?", (request.admin_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail=f"{request.role.capitalize()} not found")

        updates = []
        params = []

        # 更新用户修正的部分
        if request.name is not None:
            updates.append("name = ?")
            params.append(request.name)

        if request.email is not None:
            updates.append("email = ?")
            params.append(request.email)

        if request.phone is not None:
            updates.append("phone = ?")
            params.append(request.phone)

        if not updates:
            conn.close()
            raise HTTPException(status_code=400, detail="No fields to update")

        # 添加 admin_id 到参数列表用于 WHERE 子句
        params.append(request.admin_id)

        # 执行更新
        query = f"UPDATE {table_name} SET {', '.join(updates)} WHERE admin_id = ?"
        cursor.execute(query, params)

        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail=f"{request.role.capitalize()} not found")
        
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"Librarian {request.admin_id} update personal information"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()

        # Print to backend console
        update_data = {"admin_id": request.admin_id}
        if request.name: update_data["name"] = request.name
        if request.email: update_data["email"] = request.email
        if request.phone: update_data["phone"] = request.phone
        print(f"Updated information for {request.role} {request.admin_id}: {update_data}")

        return {
            "status": "success",
            "message": f"{request.role.capitalize()} information updated successfully"
        }

    except HTTPException:
        raise
    except sqlite3.Error as e:
        logger.error(f"Database error in update_librarian_director_information: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error updating {request.role} information: {e}")
        raise HTTPException(status_code=500, detail="Server error")