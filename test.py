import locale
import os
import sys

from dotenv import load_dotenv
import sqlite3

import exceptions
from utility import stickers_recognize

conn = sqlite3.connect(os.path.join("db", "reminders.db"))
cursor = conn.cursor()

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ACCESS_ID = os.getenv("ACCESS_ID")

print(API_TOKEN, ACCESS_ID)

def test(table: str):
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        print(row[0], row[4])
        print(stickers_recognize(row[4], row[2]))
    cursor.execute(f"SELECT * FROM sqlite_schema")
    # cursor.execute(f"SELECT name FROM sqlite_schema WHERE type IN ('table','view')")
    rows = cursor.fetchall()
    print(rows)
    print(sqlite3.sqlite_version)

test("reminder")
print(sys.getfilesystemencoding())
print(locale.getpreferredencoding())
