import os
from dotenv import load_dotenv
import sqlite3

import exceptions


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
        print(row[0], row[4])

test("reminder")
