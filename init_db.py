import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
"""
)
cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'students'")
students = [
    ("2026-00123", "Grant Padilla", "BSIT", 1, "A"),
    ("2026-00124", "Stephen jake Paclibar", "BSIT", 1, "B"),
    ("2025-00125", "Ramon Palmares", "BSIT", 2, "A"),
    ("2024-00126", "Reniel palomo", "BSIT", 3, "B"),
    ("2023-00127", "Keneth Palmes", "BSIT", 4, "A"),
]
cursor.executemany(
    """
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""",
    students,
)
conn.commit()
conn.close()
print("Database created successfully.")
