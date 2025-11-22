from annotated_types import Len
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class UpdateReaderRequest(BaseModel):
    student_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None

@router.get("/search-readers")
async def search_readers(query: str):
    """
    search readers
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Search for books by book_id, book_name, or author
        cursor.execute("""
            SELECT reader_id, student_id, name, email, phone, department, major
            FROM reader_information 
            WHERE student_id LIKE ? OR name LIKE ? OR phone LIKE ? OR email LIKE ? OR department LIKE ? OR major LIKE ?
            ORDER BY reader_id
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        # Format results as a list of dictionaries
        readers = []
        for row in results:
            reader = {
                "reader_id": row[0],
                "student_id": row[1],
                "name": row[2],
                "email": row[3],
                "phone": row[4],
                "department": row[5],
                "major": row[6]
            }
            readers.append(reader)
        
        # Print results to backend console
        print(f"Search results for '{query}': {len(readers)} readers found")
        for reader in readers:
            print(reader)
        
        return {"readers": readers}
        
    except sqlite3.Error as e:
        logger.error(f"Database error in search_readers: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error searching readers: {e}")
        raise HTTPException(status_code=500, detail="Server error")



@router.get("/add-new-reader")
async def add_new_reader(student_id: str, name: str, password: str, email: str, phone: str, department: str, major: str):
    try:
        logger.info(f"Attempting to add new reader with student_id: {student_id}, name: {name}")

        if len(student_id) != 9:
            logger.warning(f"Invalid student_id length: {student_id} (length: {len(student_id)})")
            raise HTTPException(status_code=400, detail="ID must be 9 digits")

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        logger.info("Connected to database successfully")

        # 检查是否已存在相同的 student_id
        cursor.execute("SELECT 1 FROM reader_information WHERE student_id = ?", (student_id,))
        existing_record = cursor.fetchone()
        logger.info(f"Check for existing student_id {student_id}, found: {existing_record is not None}")

        if existing_record:
            conn.close()
            logger.warning(f"Student_id {student_id} already exists in database")
            raise HTTPException(status_code=400, detail="this id already had an account")

        # 获取当前最大序号，用于生成新的 reader_id
        # 先查找所有"Reader X"格式的ID，按数值排序获取最大值
        cursor.execute("SELECT reader_id FROM reader_information WHERE reader_id LIKE 'Reader %' ORDER BY CAST(SUBSTR(reader_id, 8) AS INTEGER) DESC LIMIT 1")
        fetch_result = cursor.fetchone()
        max_reader_result = fetch_result[0] if fetch_result else None

        # 检查是否有非"Reader X"格式的ID
        cursor.execute("SELECT reader_id FROM reader_information WHERE reader_id NOT LIKE 'Reader %' ORDER BY reader_id DESC LIMIT 1")
        fetch_result2 = cursor.fetchone()
        max_other_result = fetch_result2[0] if fetch_result2 else None

        logger.info(f"Max 'Reader X' format result: {max_reader_result}")
        logger.info(f"Max other format result: {max_other_result}")

        # 确定真正的最大值
        if max_reader_result is None and max_other_result is None:
            # 如果没有任何记录，从 1 开始
            logger.info("No existing reader records found, starting with next_number = 1")
            next_number = 1
        elif max_reader_result is None:
            # 只有其他格式，按之前的逻辑处理
            max_result = max_other_result
            try:
                numbers = [int(s) for s in str(max_result).split() if s.isdigit()]
                logger.info(f"Found numbers in max_result: {numbers}")
                if numbers:
                    current_max = max(numbers)  # 使用最大的数字
                    next_number = current_max + 1
                    logger.info(f"Calculated next_number from other format: {next_number}")
                else:
                    logger.info("No numbers found in max_result, using next_number = 1")
                    next_number = 1
            except Exception as e:
                logger.warning(f"Could not parse other format max reader_id '{max_result}': {e}")
                next_number = 1
        elif max_other_result is None:
            # 只有"Reader X"格式，使用该值
            max_result = max_reader_result
            try:
                max_str = str(max_result)
                logger.info(f"Parsing max reader_id string: '{max_str}'")

                if max_str.startswith('Reader '):
                    current_max_part = max_str.split(' ')[-1]  # 获取最后一个部分（数字）
                    logger.info(f"Extracted number part: '{current_max_part}'")
                    current_max = int(current_max_part)
                    next_number = current_max + 1
                    logger.info(f"Calculated next_number from 'Reader X' format: {next_number}")
            except Exception as e:
                # 如果格式不正確或解析失败，从1开始并记录问题
                logger.warning(f"Could not parse 'Reader X' format max reader_id '{max_result}': {e}")
                next_number = 1
        else:
            # 两种格式都有，需要比较它们的数值部分
            try:
                # 解析"Reader X"格式的数字部分
                reader_max_part = max_reader_result.split(' ')[-1]
                reader_max_number = int(reader_max_part)

                # 解析其他格式中的数字
                other_numbers = [int(s) for s in str(max_other_result).split() if s.isdigit()]
                other_max_number = max(other_numbers) if other_numbers else 0

                # 使用较大的数值
                max_number = max(reader_max_number, other_max_number)
                next_number = max_number + 1
                logger.info(f"Calculated next_number by comparing both formats: {next_number}")
            except Exception as e:
                logger.warning(f"Could not compare both formats: {e}, defaulting to 'Reader X' logic")
                # 回退到"Reader X"格式的逻辑
                max_str = str(max_reader_result)
                if max_str.startswith('Reader '):
                    current_max_part = max_str.split(' ')[-1]
                    current_max = int(current_max_part)
                    next_number = current_max + 1
                    logger.info(f"Calculated next_number from 'Reader X' format: {next_number}")
                else:
                    next_number = 1

        # 生成新的 reader_id
        new_reader_id = f"Reader {next_number}"
        logger.info(f"Generated new reader_id: {new_reader_id}")

        # 插入新記錄，包含生成的 reader_id
        # 如果 name 为空或默认值，使用默认名称
        if not name or name.strip() == "":
            name = "default user name, please edit it"
            logger.info("Using default name for new reader")

        logger.info(f"Executing INSERT statement with values: reader_id={new_reader_id}, student_id={student_id}, name={name}, email={email}, phone={phone}, department={department}, major={major}")

        cursor.execute("""
            INSERT INTO reader_information(reader_id, student_id, name, password, email, phone, department, major)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (new_reader_id, student_id, name, password, email, phone, department, major))

        # 记录日志
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"librarian add new reader who has student_id = {student_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        logger.info("INSERT statement executed successfully, now committing transaction")
        conn.commit()
        logger.info("Transaction committed successfully")
        conn.close()
        logger.info(f"Database connection closed. Successfully added reader: {new_reader_id}, student_id: {student_id}")

        print(f"Add new reader: {new_reader_id}, student_id: {student_id}")

        return {
            "status": "success",
            "message": "Added successfully"
        }

    except sqlite3.Error as e:
        logger.exception(f"Database error in register_reader: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Error registering reader: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.post("/update-reader")
async def update_reader(request: UpdateReaderRequest):
    """
    Update reader information by librarian
    """
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # 检查读者是否存在
        cursor.execute("SELECT 1 FROM reader_information WHERE student_id = ?", (request.student_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Reader not found")

        # 构建更新语句
        updates = []
        params = []

        if request.name is not None:
            updates.append("name = ?")
            params.append(request.name)

        if request.email is not None:
            updates.append("email = ?")
            params.append(request.email)

        if request.phone is not None:
            updates.append("phone = ?")
            params.append(request.phone)

        if request.password is not None:
            updates.append("password = ?")
            params.append(request.password)

        if request.department is not None:
            updates.append("department = ?")
            params.append(request.department)

        if request.major is not None:
            updates.append("major = ?")
            params.append(request.major)

        if not updates:
            conn.close()
            raise HTTPException(status_code=400, detail="No fields to update")

        # 添加 student_id 到参数列表用于 WHERE 子句
        params.append(request.student_id)

        # 执行更新
        query = f"UPDATE reader_information SET {', '.join(updates)} WHERE student_id = ?"
        cursor.execute(query, params)
        
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"librarian update the information of reader who has student id = {request.student_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()

        print(f"Updated reader information for student_id: {request.student_id}")

        return {
            "status": "success",
            "message": "Reader information updated successfully"
        }

    except HTTPException:
        raise
    except sqlite3.Error as e:
        logger.error(f"Database error in update_reader: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error updating reader: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.delete("/delete-reader")
async def delete_reader(student_id: str):
    """
    Delete a reader by student_id
    Note: This will also delete related borrow records due to foreign key constraints
    """
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # 检查读者是否存在
        cursor.execute("SELECT reader_id FROM reader_information WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            raise HTTPException(status_code=404, detail="Reader not found")

        reader_id = result[0]

        # 检查是否有未归还的借阅记录
        cursor.execute("""
            SELECT COUNT(*) FROM borrow_record 
            WHERE student_id = ? AND (return_date IS NULL OR return_date = '')
        """, (student_id,))
        
        active_borrowings = cursor.fetchone()[0]
        if active_borrowings > 0:
            conn.close()
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot delete reader with {active_borrowings} active borrowing(s). Please return all books first."
            )

        # 删除借阅记录（先删除依赖记录）
        cursor.execute("DELETE FROM borrow_record WHERE student_id = ?", (student_id,))
        # 删除读者信息
        cursor.execute("DELETE FROM reader_information WHERE student_id = ?", (student_id,))

        # 日志
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"librarian deleted reader who has student id = {student_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Reader not found")

        conn.commit()
        conn.close()

        print(f"Deleted reader: {reader_id}, student_id: {student_id}")

        return {
            "status": "success",
            "message": f"Reader {student_id} deleted successfully"
        }

    except HTTPException:
        raise
    except sqlite3.Error as e:
        logger.error(f"Database error in delete_reader: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error deleting reader: {e}")
        raise HTTPException(status_code=500, detail="Server error")