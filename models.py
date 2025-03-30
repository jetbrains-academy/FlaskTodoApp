from database_initialization import db  # Import db from the new extensions module


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    todos = db.relationship('Task', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    complete = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.task} in Project {self.project_id}>'
