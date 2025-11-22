from annotated_types import Len
from fastapi import APIRouter, HTTPException
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

from pydantic import BaseModel
from typing import Optional

class UpdateBookRequest(BaseModel):
    book_id: int
    book_name: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publish_year: Optional[int] = None
    location: Optional[str] = None
    if_available: Optional[int] = None



@router.get("/libarian-add-books")
async def add_new_books(
        book_name: str,
        author: str,
        publisher: str,
        publish_year: str,
        location: str,
        if_available: int
    ):
    try:

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # 获取当前最大序号，用于生成新的 reader_id
        cursor.execute("SELECT MAX(book_id) FROM book")
        max_result = cursor.fetchone()[0]

        if max_result is None:
            # 如果还没有任何 reader 记录，从 1 开始
            new_book_id = 1
        else:
            new_book_id = max_result + 1


        cursor.execute("""
            INSERT INTO book(book_id, book_name, author, publisher, publish_year, location, if_available)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (new_book_id, book_name, author, publisher, publish_year, location, if_available))

        from datetime import datetime
        # 记录日志
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"librarian add book {new_book_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()

        print(f"book successfully added: {new_book_id}")

        return {
            "status": "success",
            "message": "New book added successfully"
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in register_reader: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error registering reader: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.post("/update-book")
async def update_book(request: UpdateBookRequest):
    """
    Update book information by librarian
    """
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # 检查图书是否存在
        cursor.execute("SELECT 1 FROM book WHERE book_id = ?", (request.book_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")

        # 构建更新语句
        updates = []
        params = []

        if request.book_name is not None:
            updates.append("book_name = ?")
            params.append(request.book_name)

        if request.author is not None:
            updates.append("author = ?")
            params.append(request.author)

        if request.publisher is not None:
            updates.append("publisher = ?")
            params.append(request.publisher)

        if request.publish_year is not None:
            updates.append("publish_year = ?")
            params.append(request.publish_year)

        if request.location is not None:
            updates.append("location = ?")
            params.append(request.location)

        if request.if_available is not None:
            updates.append("if_available = ?")
            params.append(request.if_available)

        if not updates:
            conn.close()
            raise HTTPException(status_code=400, detail="No fields to update")

        # 添加 book_id 到参数列表用于 WHERE 子句
        params.append(request.book_id)

        # 执行更新
        query = f"UPDATE book SET {', '.join(updates)} WHERE book_id = ?"
        cursor.execute(query, params)
        
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"librarian update book {request.book_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()

        print(f"Updated book information for book_id: {request.book_id}")

        return {
            "status": "success",
            "message": "Book information updated successfully"
        }

    except HTTPException:
        raise
    except sqlite3.Error as e:
        logger.error(f"Database error in update_book: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error updating book: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.delete("/delete-book")
async def delete_book(book_id: int):
    """
    Delete a book by book_id
    Note: This will also delete related borrow records due to foreign key constraints
    """
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # 检查图书是否存在
        cursor.execute("SELECT book_name FROM book WHERE book_id = ?", (book_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")

        book_name = result[0]

        # 检查是否有未归还的借阅记录
        cursor.execute("""
            SELECT COUNT(*) FROM borrow_record 
            WHERE book_id = ? AND (return_date IS NULL OR return_date = '')
        """, (book_id,))
        
        active_borrowings = cursor.fetchone()[0]
        if active_borrowings > 0:
            conn.close()
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot delete book with {active_borrowings} active borrowing(s). Please return all books first."
            )

        # 删除借阅记录（先删除依赖记录）
        cursor.execute("DELETE FROM borrow_record WHERE book_id = ?", (book_id,))

        # 删除图书信息
        cursor.execute("DELETE FROM book WHERE book_id = ?", (book_id,))

        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")

        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"librarian delete the book has ID = {book_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))
        conn.commit()
        conn.close()

        print(f"Deleted book: {book_id}, book_name: {book_name}")

        return {
            "status": "success",
            "message": f"Book {book_name} deleted successfully"
        }

    except HTTPException:
        raise
    except sqlite3.Error as e:
        logger.error(f"Database error in delete_book: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error deleting book: {e}")
        raise HTTPException(status_code=500, detail="Server error")
    


@router.get("/view-report")
async def view_library_report(date: str):
    """
    View library report including return books, No returns, borrowed books, and overdue books
    """
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # Books not returned until today (all time)
        cursor.execute("""
            SELECT b.book_name, b.author, br.student_id, br.borrow_date, br.due_date
            FROM borrow_record br
            JOIN book b ON br.book_id = b.book_id
            WHERE br.return_date IS NULL OR br.return_date = ''
        """)
        no_return_books_detail = cursor.fetchall()
        no_return_books = len(no_return_books_detail)

        # Books borrowed today
        cursor.execute("""
            SELECT b.book_name, b.author, br.student_id, br.borrow_date, br.due_date
            FROM borrow_record br
            JOIN book b ON br.book_id = b.book_id
            WHERE DATE(br.borrow_date) = DATE(?)
        """, (date,))
        borrowed_books_detail = cursor.fetchall()
        borrowed_books = len(borrowed_books_detail)

        # Books returned today
        cursor.execute("""
            SELECT b.book_name, b.author, br.student_id, br.borrow_date, br.return_date
            FROM borrow_record br
            JOIN book b ON br.book_id = b.book_id
            WHERE DATE(br.return_date) = DATE(?)
        """, (date,))
        returned_books_detail = cursor.fetchall()
        returned_books = len(returned_books_detail)

        # Overdue books as of the provided date
        cursor.execute("""
            SELECT b.book_name, b.author, br.student_id, br.borrow_date, br.due_date
            FROM borrow_record br
            JOIN book b ON br.book_id = b.book_id
            WHERE (br.return_date IS NULL OR br.return_date = '')
            AND br.due_date < DATE(?)
        """, (date,))
        overdue_books_detail = cursor.fetchall()
        overdue_books = len(overdue_books_detail)

        conn.close()

        return {
            "books didn't return until today": no_return_books,
            "books didn't return until today detail": [
                {
                    "book_name": row[0],
                    "author": row[1],
                    "student_id": row[2],
                    "borrow_date": row[3],
                    "due_date": row[4]
                } for row in no_return_books_detail
            ],
            "books borrowed today": borrowed_books,
            "books borrowed today detail": [
                {
                    "book_name": row[0],
                    "author": row[1],
                    "student_id": row[2],
                    "borrow_date": row[3],
                    "due_date": row[4]
                } for row in borrowed_books_detail
            ],
            "overdue_books": overdue_books,
            "overdue_books detail": [
                {
                    "book_name": row[0],
                    "author": row[1],
                    "student_id": row[2],
                    "borrow_date": row[3],
                    "due_date": row[4]
                } for row in overdue_books_detail
            ],
            "books returned today": returned_books,
            "books returned today detail": [
                {
                    "book_name": row[0],
                    "author": row[1],
                    "student_id": row[2],
                    "borrow_date": row[3],
                    "return_date": row[4]
                } for row in returned_books_detail
            ]
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in view_library_report: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error viewing library report: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@router.get("/view-library-logs")
async def view_library_logs(date: str):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        
        cursor.execute("""
            SELECT date, operation FROM operation_log
            WHERE DATE(date) = DATE(?)
            ORDER BY date ASC
        """, (date,))

        rows = cursor.fetchall()
        conn.close()

        logs = [{"date": r[0], "operation": r[1]} for r in rows]

        return {"date": date, "logs": logs}

    except sqlite3.Error as e:
        logger.error(f"Database error in view_library_logs: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error viewing library logs: {e}")
        raise HTTPException(status_code=500, detail="Server error")
        

