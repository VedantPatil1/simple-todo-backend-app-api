from app.models import Task
from app.serializers import task_schema


def test_serialize_task(client, set_up):
    """ Test serializer.dump returns json."""
    with client.application.app_context():
        task_object = Task(
            title='Task title',
            description='Task description',
            completed=True
        ).save()

        serialized_data = task_schema.dump(task_object)

        assert isinstance(serialized_data, dict)
        assert id is not None
        assert isinstance(serialized_data["id"], str)
        assert serialized_data["title"] == 'Task title'
        assert serialized_data['description'] == 'Task description'
        assert serialized_data['completed']


def test_serialize_list_of_tasks(client, set_up):
    """ Tests serialize a list of tasks."""
    with client.application.app_context():
        Task(title="task 1").save()
        Task(title="task 2").save()

        task_list = Task.objects()
        serialized_data = [task_schema.dump(task) for task in task_list]

        assert isinstance(serialized_data, list)
        assert len(serialized_data) == 2
        for task in serialized_data:
            assert isinstance(task, dict)
            assert "id" in task
            assert "title" in task
            assert "description" in task
            assert "completed" in task


def test_deserialize_task(client, set_up):
    """Test serializer.load retuns Task object."""
    with client.application.app_context():
        task_json = {
            'title': 'Task title',
            'description': 'Task description',
            'completed': True
        }

        deserialized_data = task_schema.load(task_json)
        deserialized_data.save()

        assert isinstance(deserialized_data, Task)
        assert deserialized_data.id is not None
        assert deserialized_data.title == "Task title"
        assert deserialized_data.description == "Task description"
        assert deserialized_data.completed


def test_empty_json_deserializes_with_default(client, set_up):
    """Test blank json input to task_schema returns Task object with default
    values."""
    with client.application.app_context():
        task_json = {}

        deserialized_data = task_schema.load(task_json)
        deserialized_data.save()

        assert isinstance(deserialized_data, Task)
        assert deserialized_data.id is not None
        assert deserialized_data.title == "Add task title"
        assert deserialized_data.description == "Add task description..."
        assert not deserialized_data.completed


def test_partial_json_deserializer_on_save(client, set_up):
    """Test partial json input to task_schema returns Task object with default
    and entered values."""
    with client.application.app_context():
        task_json = {
            'title': 'Task title',
        }
        deserialized_data = task_schema.load(task_json)
        deserialized_data.save()

        assert isinstance(deserialized_data, Task)
        assert deserialized_data.id is not None
        assert deserialized_data.title == "Task title"
        assert deserialized_data.description == "Add task description..."
        assert not deserialized_data.completed
