import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name('students.db')

students = [
    ('2026-00123', 'Ana Reyes', 'BSIT', 1, 'A'),
    ('2026-00124', 'Luis Mendoza', 'BSIT', 1, 'B'),
    ('2025-00125', 'Maya Santos', 'BSIT', 2, 'A'),
    ('2024-00126', 'Noah Garcia', 'BSIT', 3, 'B'),
    ('2023-00127', 'Ella Cruz', 'BSIT', 4, 'A'),
    ('2026-00301', 'Sofia Perez', 'BSIT', 2, 'C'),
]

with sqlite3.connect(DATABASE_PATH) as connection:
    connection.execute('DROP TABLE IF EXISTS students')
    connection.execute(
        """CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            year INTEGER NOT NULL,
            section TEXT NOT NULL,
            source TEXT DEFAULT 'Local'
        )"""
    )
    connection.executemany(
        """INSERT INTO students (student_id, name, program, year, section, source)
        VALUES (?, ?, ?, ?, ?, 'Local')""",
        students,
    )

print(f"Initialized {DATABASE_PATH} with {len(students)} local students.")
