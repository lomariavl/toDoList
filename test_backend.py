import datetime
from datetime import date, timedelta

from backend import db_create, db_delete
from backend import add_data, get_data, delete_data, update_data

today_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def test_db_create():
    db_create('todolist.db', 'daily_list')
    db_create('test2.db', 'table2')


def test_add():
    diff_datetime = str(date.today() - timedelta(days=30))
    assert add_data('', 'meeting', 0) == [1, today_datetime, '', 'meeting', 0]
    assert add_data(diff_datetime, 'meeting', 1) == [2, today_datetime, diff_datetime, 'meeting', 1]


def test_get():
    diff_datetime = str(date.today() - timedelta(days=30))
    assert get_data() == [(1, today_datetime, '', 'meeting', 0),
                          (2, today_datetime, diff_datetime, 'meeting', 1)]


def test_delete():
    assert delete_data(3) == False
    assert delete_data(4) == False


def test_update():
    diff_datetime = str(date.today() - timedelta(days=10))
    assert update_data(1, diff_datetime, 'meeting', 1) == [1, today_datetime, diff_datetime, 'meeting', 1]


def test_db_delete():
    assert db_delete('todolist.db') == True
    assert db_delete('test2.db') == True
