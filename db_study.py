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


def db_init(conn):
    query = """CREATE TABLE IF NOT EXISTS maintable 
    (maintable_id INT PRIMARY KEY AUTO_INCREMENT, 
    data1 NVARCHAR(64) NOT NULL,
    data2 INT)"""
    with conn.cursor() as cursor:
        cursor.execute(query)
        cursor.fetchall()
        conn.commit()


def db_drop(conn):
    query = "DROP TABLE IF EXISTS mydb.maintable"
    with conn.cursor() as cursor:
        cursor.execute(query)
        cursor.fetchall()
        conn.commit()


def db_initial_insert_rows(conn, count, text):
    query = 'INSERT INTO maintable (data1, data2) VALUES '
    for i in range(count - 1):
        split_begin = random.randint(0, int(len(text) / 2))
        split_end = random.randint(int(len(text) / 2), len(text) - 1)
        query += f'("{text[split_begin:split_end]}", {i+7}), '
    query += f'("{text}", {count+6});'

    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_search_key_column(conn, key):
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        for i in range(1000):
            query = f'SELECT * FROM maintable WHERE maintable_id = {random.randint(1,key)};'
            cursor.execute(query)
            cursor.fetchall()
        end = time.perf_counter_ns()
        conn.commit()
    return (end - start) / (1e6*1000)


def db_search_nonkey_column(conn, num):
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        for i in range(100):
            query = f'SELECT * FROM maintable WHERE data2 = {i+num};'
            cursor.execute(query)
            cursor.fetchall()
        end = time.perf_counter_ns()
        conn.commit()
    return (end - start) / (1e6*100)


def db_search_by_mask(conn, mask):
    query = f'SELECT * FROM maintable WHERE data1 LIKE "{mask}";'
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_insert_row(conn, text, num):
    query = f'INSERT INTO maintable (data1, data2) VALUES ("{text}", {num});'
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_insert_some_rows(conn, text, num, count):
    query = 'INSERT INTO maintable (data1, data2) VALUES '
    for i in range(count - 1):
        query += f'("{text}", {num}), '
    query += f'("{text}", {num});'
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_update_by_key_column(conn, key, text, num):
    query = f'UPDATE maintable SET data1 = "{text}", data2 = {num} WHERE maintable_id = {key};'
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_update_by_num_column(conn, text, num):
    query = f'UPDATE maintable SET data1 = "{text}" WHERE data2 = {num};'
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_delete_by_key_column(conn, key):
    query = f'DELETE FROM maintable WHERE maintable_id = {key};'
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_delete_by_num_column(conn, num):
    query = f'DELETE FROM maintable WHERE data2 = {num};'
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_delete_some_rows(conn, count):
    query = f'DELETE FROM maintable LIMIT {count};'
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_compress(conn):
    query = 'ALTER TABLE maintable ROW_FORMAT=COMPRESSED;'
    with conn.cursor() as cursor:
        start = time.perf_counter_ns()
        cursor.execute(query)
        end = time.perf_counter_ns()
        cursor.fetchall()
        conn.commit()
    return (end - start) / 1e6


def db_return_to_the_initial_state(connection, count, text):
    db_drop(connection)
    db_init(connection)
    db_initial_insert_rows(connection, count, text)


if __name__ == '__main__':
    some_num = 34
    some_text = 'ihavethreeobsessioncoffeeoneboyandsea'
    some_mask = 'k%'
    some_key = 3
    rows_group_count = 200
    con = create_connection("127.0.0.1", "root", "26081202", "mydb")
    for rows_count in [1_000, 10_000, 100_000]:
        db_return_to_the_initial_state(con, rows_count, some_text)
        print('Search key column {} rows: {:.4f} ms'.format(rows_count, db_search_key_column(con, rows_count)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        print('Search non-key column {} rows: {:.4f} ms'.format(rows_count, db_search_nonkey_column(con, some_num)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        print('Search by mask {} rows: {:.4f} ms'.format(rows_count, db_search_by_mask(con, some_mask)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        print('Insert one row {} rows: {:.4f} ms'.format(rows_count, db_insert_row(con, some_text, some_num)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        print('Insert group of rows {} rows: {:.4f} ms'.format(rows_count, db_insert_some_rows(con, some_text, some_num,
                                                                                               rows_group_count)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        print('Update key column {} rows: {:.4f} ms'.format(rows_count, db_update_by_key_column(con, some_key, some_text,
                                                                                                some_num)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        print('Update num (non-key) column {} rows: {:.4f} ms'.format(rows_count, db_update_by_num_column(con, some_text,
                                                                                                          some_num)))
        print('Delete key column {} rows: {:.4f} ms'.format(rows_count, db_delete_by_key_column(con, some_key)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        print('Delete num (non-key) column {} rows: {:.4f} ms'.format(rows_count, db_delete_by_num_column(con, some_num)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        print('Delete group of rows {} rows: {:.4f} ms'.format(rows_count, db_delete_some_rows(con, rows_group_count)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        db_delete_some_rows(con, rows_group_count)
        print('Compress db after 200 rows deletion {} rows: {} ms'.format(rows_count, db_compress(con)))
        db_return_to_the_initial_state(con, rows_group_count, some_text)
        print('Compress db with 200 rows left {} rows: {} ms'.format(rows_count, db_compress(con)))
        db_return_to_the_initial_state(con, rows_count, some_text)
        print("\n\n")