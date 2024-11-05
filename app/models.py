from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2


class User(UserMixin, db.Model):
    __tablename__ = 'User'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="niet gestart")

    earnings = db.Column(db.Float, default=0.0)

    owner_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    owner = db.relationship('User', backref='project')

    tasks = db.relationship('Task', backref='project', lazy=True)
    documents = db.relationship('Document', backref='project', lazy=True)
    notes = db.relationship('Note', backref='project', lazy=True)
    issues = db.relationship('Issue', backref='project', lazy=True)
    ideas = db.relationship('Idea', backref='project', lazy=True)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    assigned_to = db.relationship('User', backref='tasks')
class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(150), nullable=False)
    file_url = db.Column(db.String(300), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
class Issue(db.Model):
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Open')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
class Idea(db.Model):
    __tablename__ = 'ideas'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
class RegistrationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    is_used = db.Column(db.Boolean, nullable=False, default=False)
class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    quiz = db.relationship('Quiz', backref='lesson', lazy=True)
    homework = db.relationship('Homework', backref='lesson', lazy=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    questions = db.Column(db.JSON, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
class Homework(db.Model):
    __tablename__ = 'homework'

    id = db.Column(db.Integer, primary_key=True)
    assigned_task = db.Column(db.Text, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    submissions = db.relationship('HomeworkSubmission', backref='homework', lazy=True)
class HomeworkSubmission(db.Model):
    __tablename__ = 'homework_submissions'

    id = db.Column(db.Integer, primary_key=True)
    submission_content = db.Column(db.Text, nullable=False)
    submitted_by_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float, nullable=True)
class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    questionse = db.Column(db.JSON, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    submissions = db.relationship('TestSubmission', backref='test', lazy=True)
class TestSubmission(db.Model):
    __tablename__ = 'test_submissions'

    id = db.Column(db.Integer, primary_key=True)
    submitted_by_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)  # Foreign key to the Users table
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(db.Text)
    score = db.Column(db.Float, nullable=True)
class Test_Questions(db.Model):
    __tablename__ = 'test_questions'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)

    test = db.relationship('Test', backref='test_questions', lazy=True)