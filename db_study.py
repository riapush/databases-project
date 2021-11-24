import string
import random
import time

import mysql
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def insert_data(conn, n):
    letters = string.ascii_letters
    for i in range(n):
        query = f"""INSERT INTO `maintable` (Data1, Data2, Data3)
        VALUES ('{''.join(random.choice(letters) for i in range(10))}', '{''.join(random.choice(letters) for i in range(10))}', 
                '{''.join(random.choice(letters) for i in range(10))}')"""
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()


def key_search(conn, n):
    query = f"""SELECT idMainTable FROM `maintable` WHERE idMainTable = {random.randrange(0, n, 1)}"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        cursor.fetchall()
        conn.commit()
    print(f"key_search for {n}: {timer} ns")


def non_key_search(conn, n):
    query = f"""SELECT * FROM `maintable` WHERE Data2 = 'tHYcAezVkN'"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        cursor.fetchall()
        conn.commit()
    print(f"non_key_search for {n}: {timer} ns")


def mask_search(conn, n):
    query = f"""SELECT * FROM `maintable` WHERE Data2 LIKE 'A%'"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        cursor.fetchall()
        conn.commit()
    print(f"mask_search for {n}: {timer} ns")


def one_row_insert(conn, n):
    letters = string.ascii_letters
    query = f"""INSERT INTO `maintable` (Data1, Data2, Data3)
    VALUES ('{''.join(random.choice(letters) for i in range(10))}', 
    '{''.join(random.choice(letters) for i in range(10))}', '{''.join(random.choice(letters) for i in range(10))}')"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        conn.commit()
    print(f"one_row_insert for {n}: {timer} ns")


def many_rows_insert(conn, n):
    letters = string.ascii_letters
    query = f"""INSERT INTO `maintable` (Data1, Data2, Data3)
    VALUES ('{''.join(random.choice(letters) for i in range(10))}', 
    '{''.join(random.choice(letters) for i in range(10))}',
    '{''.join(random.choice(letters) for i in range(10))}'),\n"""
    for i in range(199):
        query += f"""('{''.join(random.choice(letters) for i in range(10))}',
         '{''.join(random.choice(letters) for i in range(10))}',
         '{''.join(random.choice(letters) for i in range(10))}'),\n"""
    query += f"""('{''.join(random.choice(letters) for i in range(10))}',
         '{''.join(random.choice(letters) for i in range(10))}',
         '{''.join(random.choice(letters) for i in range(10))}')"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        conn.commit()
    print(f"many_rows_insert for {n}: {timer} ns")


def row_key_update(conn, n):
    query = f"""UPDATE `maintable`
    SET Data1 = 'ABCDEFGHKL'
    WHERE idMainTable = {random.randrange(0, n, 1)}"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        conn.commit()
    print(f"row_key_update for {n}: {timer} ns")


def row_non_key_update(conn, n):
    query = f"""UPDATE `maintable`
    SET Data1 = 'ABCDEFGHKL'
    WHERE Data2 = 'anosgnxOVo'"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        conn.commit()
    print(f"row_non_key_update for {n}: {timer} ns")


def row_key_delete(conn, n):
    query = f"""DELETE FROM `maintable` WHERE idMainTable = 1"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        conn.commit()
    print(f"row_key_delete for {n}: {timer} ns")


def row_non_key_delete(conn, n):
    query = f"""DELETE FROM `maintable` WHERE Data1 = 'SyTImsYXUq'"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        conn.commit()
    print(f"row_non_key_delete for {n}: {timer} ns")


def many_rows_delete(conn,n):
    query = f"""DELETE FROM `maintable` WHERE idMainTable >= 1 AND idMainTable <= 200"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        conn.commit()
    print(f"many_rows_delete for {n}: {timer} ns")


def compress(conn, n):
    query = f"""ALTER TABLE `maintable` ROW_FORMAT=COMPRESSED"""
    with conn.cursor() as cursor:
        start_time = time.perf_counter_ns()
        cursor.execute(query)
        timer = time.perf_counter_ns() - start_time
        conn.commit()
    print(f"compress for {n}: {timer} ns")

def delete_data(conn,n):
    query = f"""DELETE FROM `maintable` WHERE idMainTable >= {n}"""
    with conn.cursor() as cursor:
        cursor.execute(query)
        conn.commit()

if __name__ == "__main__":
    conn = create_connection("127.0.0.1", "root", "26081202", "mydb")

    n = 100_000
    key_search(conn, n)
    non_key_search(conn, n)
    mask_search(conn, n)
    one_row_insert(conn, n)

    delete_data(conn, n)

    many_rows_insert(conn, n)

    delete_data(conn, n)

    row_key_update(conn, n)
    row_non_key_update(conn, n)
    row_key_delete(conn, n)

    insert_data(conn, 1)

    row_non_key_delete(conn, n)

    insert_data(conn, 1)

    many_rows_delete(conn, n)

    compress(conn, n)

    delete_data(conn, 200)

    compress(conn, n)
