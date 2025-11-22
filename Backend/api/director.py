from annotated_types import Len
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from typing import Optional
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# 搜索管理员
@router.get("/search-librarian")
async def search_librarian(query: str):
    """
    search readers
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Search for books by book_id, book_name, or author
        cursor.execute("""
            SELECT admin_id, name, email, phone, department
            FROM librarian_information 
            WHERE admin_id LIKE ? OR name LIKE ? OR phone LIKE ? OR email LIKE ?
            ORDER BY admin_id
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        # Format results as a list of dictionaries
        librarians = []
        for row in results:
            librarian = {
                "admin_id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "department": row[4]
            }
            librarians.append(librarian)
        
        # Print results to backend console
        print(f"Search results for '{query}': {len(librarians)} librarians found")
        for librarian in librarians:
            print(librarian)
        
        return {"librarians": librarians}
        
    except sqlite3.Error as e:
        logger.error(f"Database error in search_readers: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error searching readers: {e}")
        raise HTTPException(status_code=500, detail="Server error")

#删除管理员
@router.delete("/delete-librarian")
async def delete_librarian(admin_id: str):
    """
    Delete a reader by student_id
    Note: This will also delete related borrow records due to foreign key constraints
    """
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # 检查读者是否存在
        cursor.execute("SELECT admin_id FROM librarian_information WHERE admin_id = ?", (admin_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            raise HTTPException(status_code=404, detail="librarian not found")

        reader_id = result[0]


        # 删除读者信息
        cursor.execute("DELETE FROM librarian_information WHERE admin_id = ?", (admin_id,))

        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail=" not found")
        
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"director deleted the librarian {admin_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()

        print(f"Deleted librarian: {admin_id}")

        return {
            "status": "success",
            "message": f"librarian {admin_id} deleted successfully"
        }

    except HTTPException:
        raise
    except sqlite3.Error as e:
        logger.error(f"Database error in delete_reader: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error deleting reader: {e}")
        raise HTTPException(status_code=500, detail="Server error")


# 获取所有管理员
@router.get("/all-librarians")
async def get_all_librarians():
    """
    Get all librarians
    """
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT admin_id, name, email, phone, department
            FROM librarian_information
            ORDER BY admin_id
        """)

        results = cursor.fetchall()
        conn.close()

        # Format results as a list of dictionaries
        librarians = []
        for row in results:
            librarian = {
                "id": row[0],  # Use "id" for frontend consistency
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "department": row[4]
            }
            librarians.append(librarian)

        return {"librarians": librarians}

    except sqlite3.Error as e:
        logger.error(f"Database error in get_all_librarians: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error getting librarians: {e}")
        raise HTTPException(status_code=500, detail="Server error")


# 添加管理员
@router.post("/add-new-librarian")
async def add_new_librarian(
    name: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    department: str = Form(...)
):
    try:
        logger.info(f"[DEBUG] Received add-new-librarian request")
        logger.info(f"[DEBUG] Parameters received - name: '{name}' (type: {type(name)}), password: '{password[:3]}...' (type: {type(password)}), email: '{email}' (type: {type(email)}), phone: '{phone}' (type: {type(phone)}), department: '{department}' (type: {type(department)})")

        # 检查参数是否为None
        params = {'name': name, 'password': password, 'email': email, 'phone': phone, 'department': department}
        for param_name, param_value in params.items():
            if param_value is None:
                logger.error(f"[DEBUG] Parameter '{param_name}' is None")
                raise HTTPException(status_code=422, detail=f"Parameter '{param_name}' cannot be null")

        logger.info(f"Attempting to add new librarian: name={name}, email={email}, phone={phone}, department={department}")

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        logger.info("[DEBUG] Database connection established")

        # 获取当前最大序号，用于生成新的 admin_id
        cursor.execute("SELECT MAX(admin_id) FROM librarian_information")
        max_result = cursor.fetchone()[0]
        logger.info(f"[DEBUG] Query result for MAX(admin_id): {max_result} (type: {type(max_result)})")
        logger.info(f"Max admin_id from database: {max_result}")

        if max_result is None:
            # 如果还没有任何 librarian 记录，从 1 开始
            next_number = 1
            logger.info("No existing librarian records found, starting with next_number = 1")
        else:
            # 从最大 admin_id 值中计算下一个
            # 确保max_result是整数类型
            max_result_int = int(max_result) if max_result != '' else 0
            next_number = max_result_int + 1
            logger.info(f"Calculated next_number from existing records: {next_number}")

        # 检查是否已有相同ID的管理员（以防万一）
        cursor.execute("SELECT admin_id FROM librarian_information WHERE admin_id = ?", (next_number,))
        existing = cursor.fetchone()
        if existing:
            logger.warning(f"[DEBUG] Admin ID {next_number} already exists! This shouldn't happen.")

        # 插入新记录，包含生成的 admin_id
        # 如果 name 为空或默认值，使用默认名称
        if not name or name.strip() == "":
            name = "default user name, please edit it"
            logger.info("Using default name for new librarian")

        logger.info(f"[DEBUG] About to execute INSERT statement")
        logger.info(f"Inserting new librarian with admin_id={next_number}, name={name}, email={email}, phone={phone}, department={department}")
        cursor.execute("""
            INSERT INTO librarian_information(admin_id, name, password, email, phone, department)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (next_number, name, password, email, phone, department))
        logger.info(f"[DEBUG] INSERT statement executed successfully")

        # 记录日志
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"director add new librarian {next_number}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        logger.info("[DEBUG] Transaction committed")
        conn.close()
        logger.info("[DEBUG] Database connection closed")

        logger.info(f"Successfully added new librarian with admin_id: {next_number}")
        print(f"Add new librarian: {next_number}")

        return {
            "status": "success",
            "message": "Added successfully",
            "ID": next_number
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in add_new_librarian: {e}")
        logger.exception("[DEBUG] Full database error traceback:")
        raise HTTPException(status_code=500, detail="Database error")
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        logger.error(f"Error adding librarian: {e}")
        logger.exception("[DEBUG] Full error traceback:")
        raise HTTPException(status_code=500, detail="Server error")