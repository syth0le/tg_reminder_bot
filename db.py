import os
from typing import Dict, List, Tuple

import sqlite3

import exceptions


conn = sqlite3.connect(os.path.join("db", "reminders.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()
    pass


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
    cursor.execute(f"delete from {table} where is_done = 1")
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
        return to_delete

def update(table: str, row_id: int) -> Tuple:
# UPDATE Customers SET ContactName = 'Alfred Schmidt', City= 'Frankfurt' WHERE CustomerID = 1;
    row_id = int(row_id)
    cursor.execute(f"UPDATE {table} SET is_done=1 where id={row_id}")
    conn.commit()

    cursor.execute(f"SELECT * FROM {table} where id={row_id}")
    updated = cursor.fetchone()
    if updated is None:
        raise exceptions.NotConsistInDB("this id db doesn't include")    
    return updated


def get_cursor():
    return cursor


def _init_db():
    """database initialization"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """checks db initialization, if not — makes initialization"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='reminder'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()
