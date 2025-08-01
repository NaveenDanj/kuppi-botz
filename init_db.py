import sqlite3

conn = sqlite3.connect('materials.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY,
    title TEXT,
    course TEXT,
    type TEXT,
    semester TEXT,
    year TEXT,
    drive_link TEXT
)''')

materials = [
    ("Week 1 Notes - CS101", "CS101", "notes", "1" ,"1", "https://drive.google.com/file/d/abc123/view?usp=sharing"),
    ("Midterm Paper 2023 - CS101", "CS101", "papers", "2" ,"2", "https://drive.google.com/file/d/xyz456/view?usp=sharing"),
]


c.executemany('INSERT INTO materials (title, course, type, semester , year, drive_link) VALUES (?, ?, ?, ?, ? , ?)', materials)

conn.commit()
conn.close()