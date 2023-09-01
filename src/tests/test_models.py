"""
Tests for models.
"""

from app.models import Task


def test_get_task_by_id(client, set_up):
    """Test get test by id."""
    with client.application.app_context():
        Task(
            title="Test Task Title.",
            description="Test Task Description",
            completed=True,
        ).save()
        task_id = Task.objects.get(title='Test Task Title.').id

        task = Task.objects.get(id=str(task_id))

        assert task.title == 'Test Task Title.'
        assert task.description == 'Test Task Description'
        assert task.completed


def test_get_task_by_title(client, set_up):
    """test to get tasks from db for given task name."""
    with client.application.app_context():
        Task(title="title").save()
        Task(title="title").save()
        tasks = Task.objects.filter(title='title')

        assert len(tasks) == 2
        task_ids = []
        for task in tasks:
            assert task.title == 'title'
            task_ids.append(task.id)

        assert not task_ids[0] == task_ids[1]


def test_create_task(client, set_up):
    """test create task with no args uses default values."""
    with client.application.app_context():
        task = Task().save()

        assert task.id is not None
        assert task.title == "Add Task Title"
        assert task.description == "Add task description..."
        assert not task.completed


def test_update_task_details(client, set_up):
    """test updating tasks after being created."""
    with client.application.app_context():
        task = Task(title="test title").save()

        task.title = 'updated task title'
        task.description = 'updated task description'
        task.completed = True

        task.save()

        assert task.title == 'updated task title'
        assert task.description == 'updated task description'
        assert task.completed


def test_delete_task(client, set_up):
    with client.application.app_context():
        task = Task().save()
        task_id = task.id
        task.delete()

        assert len(Task.objects(id=task_id)) == 0
