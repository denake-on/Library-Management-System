import sqlite3
import os
from datetime import datetime



def insert_sample_borrow_records(db_path: str):
    """Ensure `borrow_record` exists and insert three sample borrow rows.

    Uses INSERT OR IGNORE semantics by making `record_id` the PRIMARY KEY
    so repeated runs won't create duplicates for the same `record_id`.
    """
    borrow_rows = [
        (31, '123090404', 193, '2025-07-20', '2025-08-19', '2025-08-15', 1),
        (32, '123090404', 194, '2025-08-20', '2025-09-19', '2025-09-15', 1),
        (33, '123090404', 195, '2025-09-09', '2025-09-29', '2025-09-15', 0),
    ]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    try:
        # Use INSERT OR IGNORE to avoid duplicate primary-key errors on repeated runs
        cursor.executemany(
            """
            INSERT OR IGNORE INTO borrow_record
            (record_id, student_id, book_id, borrow_date, due_date, return_date, renew)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            borrow_rows,
        )
        conn.commit()
        print(f"Inserted/ignored {len(borrow_rows)} borrow_record rows into {db_path}")
    except sqlite3.Error as e:
        print(f"Error inserting borrow_record rows: {e}")
    finally:
        conn.close()


def main():
    db_path = "library.db"

    # Ensure DB file exists (will be created by sqlite if missing)
    print(f"Opening database: {os.path.abspath(db_path)}")
    insert_sample_borrow_records(db_path)
    print("Done.")


if __name__ == "__main__":
    main()