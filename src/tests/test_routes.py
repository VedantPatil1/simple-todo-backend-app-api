from app.models import Task


def test_get_tasks(client, set_up):
    Task(title="Task 1").save()

    response = client.get('/api/task_list')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert 'message' in data
    assert 'task list' in data
    assert isinstance(data['task list'], list)
    assert len(data['task list']) == 1
    assert data['task list'][0]['title'] == 'Task 1'


def test_get_task(client, set_up):
    task = Task().save()
    task_id = str(task.id)

    response = client.get(f'api/task/{task_id}')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(response.data, bytes)
    assert isinstance(data, dict)
    assert 'message' in data
    assert data['message'] == 'Task found!!'
    assert 'id' in data['task']
    assert 'title' in data['task']
    assert 'description' in data['task']
    assert 'completed' in data['task']
    assert data['task']['id'] == task_id


def test_get_task_returns_error_if_no_id(client, set_up):
    invalid_id = '1a5b8f7d3e0c9a2b4f6d8e1c'
    response = client.get(f'api/task/{invalid_id}')
    data = response.get_json()

    assert response.status_code == 404
    assert 'error' in data
    assert 'message' in data
    assert data['message'] == f'No task found with task is: {invalid_id}'


def test_create_task(client, set_up):
    payload = {
        'title': 'Task title',
        'description': 'Task description',
        'completed': 'true'
    }
    response = client.post('api/task', json=payload)
    data = response.get_json()

    task = Task.objects().first()

    assert response.status_code == 201
    assert 'message' in data
    assert 'task' in data

    assert task is not None
    assert str(task.id) == data['task']['id']
    assert task.title == data['task']['title']
    assert task.description == data['task']['description']
    assert task.completed == data['task']['completed']


def test_create_task_with_no_input(client, set_up):
    payload = {}
    response = client.post('api/task', json=payload)
    data = response.get_json()

    task = Task.objects().first()

    assert response.status_code == 201
    assert 'message' in data
    assert 'task' in data

    assert task is not None
    assert task.title == 'Add task title'
    assert task.description == 'Add task description...'
    assert not task.completed

    assert str(task.id) == data['task']['id']
    assert task.title == data['task']['title']
    assert task.description == data['task']['description']
    assert task.completed == data['task']['completed']


def test_update_task(client, set_up):
    task = Task().save()
    task_id = str(task.id)

    payload = {
        "title": "updated title",
        "description": "updated description",
    }
    response = client.put(f'api/task/{task_id}', json=payload)
    data = response.get_json()

    task = Task.objects.get(id=task_id)

    assert response.status_code == 200
    assert 'message' in data
    assert 'task' in data

    assert task.title == payload['title']
    assert task.description == payload['description']

    assert str(task.id) == data['task']['id']
    assert task.title == data['task']['title']
    assert task.description == data['task']['description']
    assert task.completed == data['task']['completed']


def test_update_task_returns_error_if_no_id(client, set_up):
    invalid_id = '1a5b8f7d3e0c9a2b4f6d8e1c'
    payload = {}
    response = client.put(f'api/task/{invalid_id}', json=payload)
    data = response.get_json()

    assert response.status_code == 404
    assert 'error' in data
    assert 'message' in data
    assert data['message'] == f'No task found with task is: {invalid_id}'


def test_delete_task(client):
    task = Task().save()
    task_id = str(task.id)
    response = client.delete(f'api/task/{task_id}')
    data = response.get_json()

    task = Task.objects(id=task_id).first()

    assert response.status_code == 200
    assert 'message' in data

    assert task is None


def test_delete_task_returns_error_if_no_id(client, set_up):
    invalid_id = '1a5b8f7d3e0c9a2b4f6d8e1c'
    response = client.delete(f'api/task/{invalid_id}')
    data = response.get_json()

    assert response.status_code == 404
    assert 'error' in data
    assert 'message' in data
    assert data['message'] == f'No task found with task is: {invalid_id}'
