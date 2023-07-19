import sqlite3
import os
from werkzeug.exceptions import abort


def script_table(name_t) -> str:
    script = "CREATE TABLE " + name_t + \
             " (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, " \
             "date_created DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')), " \
             "date_finished DATETIME, " \
             "title TEXT, " \
             "status INTEGER)"
    return script


def db_create(database_name, table_name):
    try:
        con = sqlite3.connect(database_name)
        cur = con.cursor()

        row = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)",
                          (table_name,)).fetchone()
        if row is None:
            add = cur.execute(script_table(table_name))
            con.commit()
        con.close()
    except sqlite3.DatabaseError:
        abort(404)


def db_delete(database_name) -> bool:
    if os.path.isfile(database_name):
        os.remove(database_name)
        return True
    return False


def db_connection():
    con = sqlite3.connect('todolist.db')
    return con


def get_data():
    con = db_connection()
    records = con.execute('SELECT * FROM daily_list').fetchall()
    con.close()
    return records


def get_post(post_id):
    con = db_connection()
    data = con.execute('SELECT * FROM daily_list WHERE id=?',
                       (post_id,)).fetchall()
    con.close()
    return data


def add_data(date_finished, title, status):
    con = db_connection()
    cur = con.cursor()
    cur.execute('INSERT INTO daily_list (date_finished, title, status) '
                'VALUES (?,?,?) RETURNING *',
                (date_finished, title, status,))
    new_post = cur.fetchone()
    con.commit()
    con.close()
    return list(new_post)


def delete_data(post_id) -> bool:
    con = db_connection()
    cur = con.cursor()
    delete = cur.execute('DELETE FROM daily_list '
                         'WHERE id=?',
                         (post_id,))
    row_affected = delete.rowcount
    con.commit()
    con.close()
    return row_affected > 0


def update_data(post_id, date_finished, title, status):
    con = db_connection()
    cur = con.cursor()
    update = cur.execute('UPDATE daily_list '
                         'SET (date_finished, title, status) = (?,?,?) '
                         'WHERE id=? RETURNING *',
                         (date_finished, title, status, post_id))
    rewrite_post = cur.fetchone()
    con.commit()
    con.close()
    return list(rewrite_post)
