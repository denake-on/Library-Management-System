from fastapi import APIRouter, HTTPException
import sqlite3
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/search-books")
async def search_books(query: str):
    """
    Search for books based on a query string
    The query will match against book_id, book_name, and author
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Search for books by book_id, book_name, or author
        cursor.execute("""
            SELECT book_id, book_name, author, publisher, publish_year, location, if_available
            FROM book 
            WHERE book_id LIKE ? OR book_name LIKE ? OR author LIKE ?
            ORDER BY book_name
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        # Format results as a list of dictionaries
        books = []
        for row in results:
            book = {
                "book_id": row[0],
                "book_name": row[1],
                "author": row[2],
                "publisher": row[3],
                "publish_year": row[4],
                "location": row[5],
                "if_available": row[6]
            }
            books.append(book)
        
        # Print results to backend console
        print(f"Search results for '{query}': {len(books)} books found")
        for book in books:
            print(book)
        
        return {"books": books}
        
    except sqlite3.Error as e:
        logger.error(f"Database error in search_books: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error searching books: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@router.get("/reader-borrowings")
async def get_reader_borrowings(student_id: str):
    """
    Get borrowing records for a specific reader by their student ID
    """
    try:
        print("ID")
        print(student_id)
        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Get borrowing records for the student, join with book information
        cursor.execute("""
            SELECT
                br.record_id, 
                br.student_id,
                br.book_id,
                br.borrow_date,
                br.due_date,
                br.return_date,
                br.renew,
                b.book_name,
                b.author
            FROM borrow_record br
            JOIN book b ON br.book_id = b.book_id
            WHERE br.student_id = ?
            ORDER BY br.borrow_date DESC
        """, (student_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        # Format results as a list of dictionaries
        borrowings = []
        for row in results:
            borrowing = {
                "borrow_id": row[0],  # Using borrow_id to match frontend expectations
                "student_id": row[1],
                "book_id": row[2],
                "borrow_date": row[3],
                "due_date": row[4],
                "return_date": row[5],
                "renew": row[6],
                "book_name": row[7],
                "author": row[8]
            }
            borrowings.append(borrowing)
        
        # Print results to backend console
        print(f"Found {len(borrowings)} borrowings for student {student_id}")
        for borrowing in borrowings:
            print(borrowing)
        
        return {"borrowings": borrowings}
        
    except sqlite3.Error as e:
        logger.error(f"Database error in get_reader_borrowings: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error getting reader borrowings: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/reader-activity-calendar")
async def get_reader_activity_calendar(student_id: str):
    """
    Get reading activity calendar data for a specific reader
    Returns dates and activity counts for the calendar visualization
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # Get borrowing records grouped by date for the student
        cursor.execute("""
            SELECT
                borrow_date,
                COUNT(*) as activity_count
            FROM borrow_record
            WHERE student_id = ?
            GROUP BY borrow_date
        """, (student_id,))

        results = cursor.fetchall()
        conn.close()

        # Format results as a dictionary of date -> count
        activity_data = {}
        for row in results:
            date = row[0]
            count = row[1]
            activity_data[date] = count

        # Print results to backend console
        print(f"Found activity data for student {student_id}: {activity_data}")

        return {"activity_data": activity_data}

    except sqlite3.Error as e:
        logger.error(f"Database error in get_reader_activity_calendar: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error getting reader activity calendar: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.post("/borrow-book")
async def borrow_book(student_id: str, book_id: int):
    """
    Borrow a book: update book availability and create a borrow record
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # Check if book is available
        cursor.execute("SELECT if_available FROM book WHERE book_id = ?", (book_id,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")

        if_available = result[0]
        if if_available != 1:
            conn.close()
            raise HTTPException(status_code=400, detail="Book is not available for borrowing")


        cursor.execute("UPDATE book SET if_available = 0 WHERE book_id = ?", (book_id,))


        from datetime import datetime, timedelta
        borrow_date = datetime.now().strftime('%Y-%m-%d')

        due_date = (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d')


        cursor.execute("""
            INSERT INTO borrow_record (student_id, book_id, borrow_date, due_date, renew)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, book_id, borrow_date, due_date, 0))

        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"Student {student_id} borrowed book {book_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()


        print(f"Book {book_id} borrowed by student {student_id} on {borrow_date}, due {due_date}")

        return {
            "status": "success",
            "message": f"Successfully borrowed book {book_id}",
            "borrow_date": borrow_date,
            "due_date": due_date
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in borrow_book: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error borrowing book: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@router.get("/reader-reading-report")
async def get_reading_report_information(student_id: str):
    """
    Generate up to two personalized reading report sentences for a reader.
    """
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                br.borrow_date,
                br.book_id,
                br.return_date,
                b.book_name
            FROM borrow_record br
            JOIN book b ON br.book_id = b.book_id
            WHERE br.student_id = ?
            ORDER BY br.borrow_date DESC
        """, (student_id,))

        results = cursor.fetchall()
        conn.close()

        if not results:
            return {"reports": ["please read more books"]}

        def parse_date(date_str):
            if not date_str:
                return None
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return None

        def format_month_day(date_obj):
            if not date_obj:
                return "Someday"
            month = date_obj.strftime("%B")
            day = date_obj.day
            suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
            return f"{month} {day}{suffix}"

        # Group by borrow date to find multi-book checkouts
        day_groups = {}
        for borrow_date, _, _, book_name in results:
            date_key = parse_date(borrow_date)
            if not date_key:
                continue
            day_groups.setdefault(date_key, []).append(book_name)

        reports = []

        # Template 1: day with most books
        if day_groups:
            top_day, books_on_day = max(day_groups.items(), key=lambda item: len(item[1]))
            if len(books_on_day) >= 2:
                books_list = ", ".join(books_on_day[:5])
                reports.append(
                    f"On {format_month_day(top_day)}, you checked out {len(books_on_day)} books at once — {books_list}. Maybe they sparked a few new ideas."
                )

        # Template 2: book with longest engagement in last 3 months
        three_months_ago = datetime.today().date() - timedelta(days=90)
        engagement = {}
        for borrow_date, _, return_date, book_name in results:
            borrow_dt = parse_date(borrow_date)
            if not borrow_dt or borrow_dt < three_months_ago:
                continue
            return_dt = parse_date(return_date) or datetime.today().date()
            duration = max((return_dt - borrow_dt).days, 1)
            engagement[book_name] = engagement.get(book_name, 0) + duration

        if engagement:
            favorite_book = max(engagement.items(), key=lambda item: item[1])[0]
            reports.append(
                f"Over the past three months, the book you spent the most time with was {favorite_book} — clearly a favorite in your recent reading history."
            )

        if not reports:
            return {"reports": ["please read more books"]}

        print(reports)
        return {"reports": reports[:2]}

    except sqlite3.Error as e:
        logger.error(f"Database error in get_reading_report_information: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error generating reading report: {e}")
        raise HTTPException(status_code=500, detail="Server error")

@router.get("/reader-return-books")
async def return_book(student_id: str, book_id: int):
    """
    Return a book: update book availability and update a borrow record
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # where的三个条件 student id和book_id可能会重复防止一个学生多次借阅同一本书
        cursor.execute("""
            SELECT borrow_date, due_date
            FROM borrow_record
            WHERE student_id = ?
              AND book_id = ?
              AND (return_date IS NULL OR return_date = '')
        """, (student_id, book_id))

        borrow_record = cursor.fetchone()

        if not borrow_record:
            conn.close()
            raise HTTPException(status_code=404, detail="Borrow record not found or already returned")


        cursor.execute("UPDATE book SET if_available = 1 WHERE book_id = ?", (book_id,))


        from datetime import datetime
        return_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            UPDATE borrow_record
            SET return_date = ?
            WHERE student_id = ? 
            AND book_id = ? 
            AND (return_date IS NULL OR return_date = '')
        """, (return_date, student_id, book_id))

        # 记录日志
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"Student {student_id} returned book {book_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()

        print(f"Book {book_id} returned by student {student_id} on {return_date}")

        return {
            "status": "success",
            "message": f"Successfully returned book {book_id}",
            "return_date": return_date,
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in return_book: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error returning book: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/reader-renew-books")
async def renew_book(student_id: str, book_id: int):
    """
    Renew a book: update a borrow record
    """
    try:
        from datetime import datetime, timedelta

        # Connect to SQLite database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        # Get the current due date to calculate the new extended due date
        cursor.execute("""
            SELECT borrow_date, due_date
            FROM borrow_record
            WHERE student_id = ?
              AND book_id = ?
              AND (return_date IS NULL OR return_date = '')
              AND renew = 0
        """, (student_id, book_id))

        borrow_record = cursor.fetchone()

        if not borrow_record:
            conn.close()
            raise HTTPException(status_code=404, detail="This book can not be renewed")

        original_due_date_str = borrow_record[1]

        # Parse the original due date and add 10 days to it
        try:
            original_due_date = datetime.strptime(original_due_date_str, '%Y-%m-%d')
            new_due_date = original_due_date + timedelta(days=10)
            new_due_date_str = new_due_date.strftime('%Y-%m-%d')
        except ValueError:
            # If there's an issue with date parsing, add 10 days from today
            new_due_date = datetime.now() + timedelta(days=10)
            new_due_date_str = new_due_date.strftime('%Y-%m-%d')

        # Update the borrow record with renew = 1 and the extended due date
        cursor.execute("""
            UPDATE borrow_record
            SET renew = 1, due_date = ?
            WHERE student_id = ?
            AND book_id = ?
            AND (return_date IS NULL OR return_date = '')
        """, (new_due_date_str, student_id, book_id))

        # 记录日志
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operation = f"Student {student_id} renewed book {book_id}"

        cursor.execute("""
            INSERT INTO operation_log (date, operation)
            VALUES (?, ?)
        """, (date, operation))

        conn.commit()
        conn.close()

        print(f"Book {book_id} renewed by student {student_id}, new due date: {new_due_date_str}")

        return {
            "status": "success",
            "message": f"Successfully renewed book {book_id}",
            "new_due_date": new_due_date_str
        }

    except sqlite3.Error as e:
        logger.error(f"Database error in renew_book: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error renewing book: {e}")
        raise HTTPException(status_code=500, detail="Server error")