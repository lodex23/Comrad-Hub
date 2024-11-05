from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import psycopg2
from app.models import User, Test

class RegistrationForm(FlaskForm):
    Name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    token = StringField('Registration Token', validators=[DataRequired()])
    submit = SubmitField('Register')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Email niet gevonden!")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
class CreateProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create Project')
class CreateLessonForm(FlaskForm):
    title = StringField('Lesson Title', validators=[DataRequired()])
    description = TextAreaField('Lesson Description', validators=[DataRequired()])
    content = TextAreaField('Lesson Content', validators=[DataRequired()])
    submit = SubmitField('Create Lesson')
class CreateHomeworkForm(FlaskForm):
    assigned_task = TextAreaField('Assigned Task', validators=[DataRequired()])
    submit = SubmitField('Assign Homework')
class CreateTestForm(FlaskForm):
    questions = TextAreaField('Questions', validators=[DataRequired()])
    submit = SubmitField('Create Test')
class QuestionForm(FlaskForm):
    question_text = StringField('Question Text', validators=[DataRequired()])
    question_type = SelectField('Question Type', choices=[
        ('string', 'String Input'),
        ('mcq', 'Multiple Choice'),
        ('yes_no', 'Yes/No'),
        ('boolean', 'True/False'),
        ('textarea', 'Text Area')
    ])
    options = StringField('Options (comma-separated)')  # Only used for MCQs
class CreateQuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired()])
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    submit = SubmitField('Create Quiz')
class HomeworkSubmissionForm(FlaskForm):
    submission_content = TextAreaField('Your Homework Submission', validators=[DataRequired()])
    submit = SubmitField('Submit Homework')
class TestSubmissionForm(FlaskForm):
    answers = TextAreaField('Test Answers (JSON Format)', validators=[DataRequired()])
    submit = SubmitField('Submit Test')

class TestResultForm(FlaskForm):
    user_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    Test_id = SelectField('Test', coerce=int, validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    comments = TextAreaField('Comments')
    submit = SubmitField('Submit result')

    def __init__(self, *args, **kwargs):
        super(TestResultForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]
        self.Test_id.choices = [tests.id for tests in Test.query.all()]

