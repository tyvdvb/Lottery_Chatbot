import sqlite3

conn = sqlite3.connect("lottery.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS winning_numbers(
          draw_date TEXT, 
          numbers TEXT,
          jackpot_amount REAL
          ) 
"""
)

c.executemany("INSERT INTO winning_numbers VALUES (?,?,?)", [
    ("2025-09-01", "3, 12, 18, 27, 42, 49", 1000000),
    ("2025-09-04", "5, 14, 11, 17, 51, 12", 750000),
    ("2025-09-07", "11, 7, 12, 21, 8, 57", 1200000),
    ("2025-09-10", "8, 1, 23, 7, 14, 9", 900000),
    ("2025-09-13", "2, 19, 21, 33, 40, 48", 1100000),
    ("2025-09-16", "6, 13, 22, 28, 35, 50", 800000),
    ("2025-09-19", "4, 15, 20, 26, 39, 45", 950000),
    ("2025-09-22", "1, 9, 14, 23, 37, 44", 1250000),
])

c.execute("""
CREATE TABLE IF NOT EXISTS faq(
          question TEXT,
          answer Text
          )
""")


c.executemany("INSERT INTO faq VALUES (?,?)", [
    ("How old do you need to be to play?", "You must be 18 years or older to play"),
    ("Where can I buy tickets?", "Tickets can be purchased at authorized retailers or online"),
    ("What is the jackpot?", "The jackpot is the top prize for matching all winning numbers"),
])

conn.commit()
conn.close()
