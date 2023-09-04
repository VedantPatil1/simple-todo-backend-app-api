from flask import Blueprint, jsonify, request
from mongoengine.errors import DoesNotExist

from app.models import Task
from app.serializers import task_schema


tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route("/task_list", methods=['GET'])
def get_task_list():
    task_list = Task.objects()
    serialized_task_list = [task_schema.dump(task) for task in task_list]
    response_data = {
        "message": f"{len(serialized_task_list)} tasks found.",
        "task list": serialized_task_list,
    }
    return jsonify(response_data), 200


@tasks_bp.route("/task/<id>", methods=['GET'])
def get_task(id):
    try:
        task = Task.objects.get(id=id)
        serialized_task = task_schema.dump(task)
        response_data = {
            'message': 'Task found!!',
            'task': serialized_task,
        }
        return jsonify(response_data), 200
    except DoesNotExist as e:
        response_data = {
            'message': f'No task found with task is: {id}',
            'error': str(e),
        }
        return jsonify(response_data), 404


@tasks_bp.route("/task", methods=['POST'])
def create_task():
    data = request.get_json()
    task = task_schema.load(data)
    task.save()
    response_data = {
        'message': 'Task created Succesfully!!',
        'task': task_schema.dump(task),
    }
    return jsonify(response_data), 201


@tasks_bp.route("/task/<id>", methods=['PUT'])
def update_task(id):
    try:
        data = request.get_json()
        task = Task.objects.get(id=id)
        for field in data:
            setattr(task, field, data[field])

        task.save()
        response_data = {
            'message': 'Task Updated!!',
            'task': task_schema.dump(task),
        }
        return jsonify(response_data), 200
    except DoesNotExist as e:
        response_data = {
            'message': f'No task found with task is: {id}',
            'error': str(e),
        }
        return jsonify(response_data), 404


@tasks_bp.route("/task/<id>", methods=['DELETE'])
def delete_task(id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        response_data = {
            'message': 'Task Deleted!!'
        }
        return jsonify(response_data), 200
    except DoesNotExist as e:
        response_data = {
            'message': f'No task found with task is: {id}',
            'error': str(e),
        }
        return jsonify(response_data), 404
