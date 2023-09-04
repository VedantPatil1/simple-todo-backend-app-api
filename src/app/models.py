from flask_mongoengine import MongoEngine


db = MongoEngine()


class Task(db.Document):
    title = db.StringField(max_length=80, default="Add task title")
    description = db.StringField(default="Add task description...")
    completed = db.BooleanField(default=False)
