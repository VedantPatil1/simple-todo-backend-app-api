from marshmallow_mongoengine import ModelSchema

from app.models import Task


class TaskSchema(ModelSchema):
    class Meta:
        model = Task


task_schema = TaskSchema()
