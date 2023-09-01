from app import db


class Task(db.Document):
    title = db.StringField(max_length=80, default="Add Task Title")
    description = db.StringField(default="Add task description...")
    completed = db.BooleanField(default=False)