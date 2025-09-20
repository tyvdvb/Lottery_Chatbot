import sqlite3

conn = sqlite3.connect("lottery.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS winning_numbers(
          draw_date TEXT, 
          numbers TEXT
          ) 
"""
)

c.executemany("INSERT INTO winning_numbers VALUES (?,?)", [
    ("2025-09-07", "3, 12, 18, 27, 42, 49"),
    ("2025-09-10", "5, 14, 11, 17, 51, 12"),
    ("2025-09-13", "11, 7, 12, 21, 8, 57"),
    ("2025-09-16", "8, 1, 23, 76, 14, 9")
])

c.execute("""
CREATE TABLE IF NOT EXISTS faq(
          question TEXT,
          answer Text
          )
""")


c.executemany("INSERT INTO faq VALUES (?,?)", [
    ("How old do you need to be to play?", "You must be 18 years or older to play")
])

conn.commit()
conn.close()
