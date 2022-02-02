import sqlite3

def use_connection(conn):
    rows = conn.execute("SELECT * FROM students;")
    length = 0
    for row in rows:
        length += 1
    return length