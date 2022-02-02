import sqlite3

def build_database(filename):
    conn = sqlite3.connect(filename)
    conn.execute("CREATE TABLE students (name TEXT, points INTEGER);")
    conn.execute("INSERT INTO students VALUES ('Josh', 45);")
    conn.execute("INSERT INTO students VALUES ('Dennis', 62);")
    conn.execute("INSERT INTO students VALUES ('Cam', 42);")
    conn.execute("INSERT INTO students VALUES ('Jie', 83);")
    conn.execute("INSERT INTO students VALUES ('Zizhen', 92);")
    conn.execute("INSERT INTO students VALUES ('Sadie', 76);")
    conn.commit()
    conn.close()