from datetime import datetime

from flask import Blueprint, request

from backend import db_create, get_data, add_data, update_data, delete_data, get_post

bp = Blueprint('bp', __name__, url_prefix='/api/todolist')


@bp.get('/')
def get_data_db():
    db_create('todolist.db', 'daily_list')
    data = get_data()
    return data


@bp.get('/<int:daily_list_id>')
def get_by_id(daily_list_id):
    data = get_post(daily_list_id)
    return data


@bp.post('/')
def post():
    req_json = request.json
    title = req_json['title']
    status = req_json['status']
    date_finished = None
    if status:
        date_finished = datetime.now().ctime()
    new_post = add_data(date_finished, title, status)
    return new_post


@bp.patch('/updateStatus')
def patch():
    url_param = request.args
    daily_list_id = url_param['id']
    record = get_by_id(daily_list_id)
    if not record:
        return 'Record not exist!'

    req_json = request.json
    title = req_json['title']
    status = req_json['status']
    date_finished = None
    if status:
        date_finished = datetime.now().ctime()
    record = update_data(daily_list_id, date_finished, title, status)
    return record


@bp.delete('/<int:daily_list_id>')
def delete(daily_list_id):
    status = delete_data(daily_list_id)
    return 'Record was' + (' deleted successful!' if status > 0 else ' not deleted!')
