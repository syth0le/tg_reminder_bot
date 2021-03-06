import os
import sqlite3
from datetime import timedelta
from dateutil.parser import parse
from typing import Dict, List, Tuple

from app import exceptions

conn = sqlite3.connect(os.path.join("db", "reminders.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict) -> object:
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()

    cursor.execute(f"SELECT * FROM {table} ORDER BY id DESC")
    row = cursor.fetchone()
    return row


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def clean_done(table: str) -> None:
    is_done = 1
    cursor.execute(f"delete from {table} where is_done={is_done}")
    conn.commit()


def delete(table: str, row_id: int) -> Tuple:
    row_id = int(row_id)
    cursor.execute(f"SELECT * FROM {table} where id={row_id}")
    to_delete = cursor.fetchone()
    if to_delete is None:
        raise exceptions.NotConsistInDB("this id db doesn't include")
    else:
        cursor.execute(f"delete from {table} where id={row_id}")
        conn.commit()
        return from_db_unpack(to_delete, with_id=True)


def update(table: str, row_id: int) -> Tuple:
    row_id = int(row_id)
    print(row_id)
    cursor.execute(f"UPDATE {table} SET is_done=1 where id={row_id}")
    conn.commit()

    cursor.execute(f"SELECT * FROM {table} where id={row_id}")
    updated = cursor.fetchone()
    if updated is None:
        print("sdjlnkasfvk")
        raise exceptions.NotConsistInDB("this id db doesn't include")
    return from_db_unpack(updated, with_id=True)


def extend_by_id(table: str, row_id: int, date: str, frequency: int) -> None:
    row_id = int(row_id)
    frequency = timedelta(minutes=frequency)
    temp = date.split(" ")
    hours, minutes, seconds = map(int, temp[1].split(":"))
    date = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    date = temp[0] + ' ' + str(date + frequency)
    date = parse(date, fuzzy=True)
    print(date, type(date))
    cursor.execute(f"UPDATE {table} SET date_time = :date where id={row_id}", {'date': date})
    conn.commit()


def find_by_date(table: str, date: str) -> List[Tuple]:
    cursor.execute(f"SELECT * FROM {table} WHERE date_time = :date", {'date': date})
    rows = cursor.fetchall()
    return rows


def find_by_id(table: str, id: int) -> object:
    cursor.execute(f"SELECT * FROM {table} WHERE id ={id}")
    row = cursor.fetchone()
    return row


def get_cursor() -> cursor:
    return cursor


def from_db_unpack(obj, with_id: bool = False) -> list:
    # print(obj, type(obj))
    id = obj[0]
    title = obj[1]
    category = obj[2]
    date = obj[3]
    is_done = obj[4]
    frequency = obj[5]
    if with_id:
        return id, title, category, date, is_done, frequency
    else:
        return title, category, date, is_done, frequency


def _init_db() -> None:
    """database initialization"""
    file = os.path.join("db", "createdb.sql")
    with open(file, "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists() -> None:
    """checks db initialization, if not ??? makes initialization"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='reminder'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
