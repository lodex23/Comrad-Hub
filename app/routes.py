from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.models import Project, Task, Note, Issue, RegistrationToken, User, Document, Lesson, Homework, Quiz, Test, HomeworkSubmission, TestSubmission
from app.forms import RegistrationForm, LoginForm, CreateProjectForm, CreateLessonForm, CreateHomeworkForm, CreateQuizForm, CreateTestForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import email
import psycopg2
from markdown2 import markdown
from app.forms import TestResultForm


bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid username or password", 'danger')

    return render_template('index.html', form=form)
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the token is valid and unused
        token = RegistrationToken.query.filter_by(token=form.token.data, is_used=False).first()
        if not token:
            flash('Invalid or used registration token', 'danger')
            return redirect(url_for('main.register'))

        # Proceed with registration if token is valid
        user = User(name=form.Name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)

        # Mark the token as used
        token.is_used = True
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form)
@login_required
@bp.route('/Dashboard', methods=['GET', 'POST'])
def dashboard():
    print(current_user.name)
    return render_template("Dashboard.html")
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
@bp.route("/projects", methods=['GET'])
@login_required
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)
@bp.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = CreateProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data, owner_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('main.projects'))
    return render_template('add_project.html', form=form)
@bp.route("/project_dashboard", methods=['GET', 'POST'])
@login_required
def project_dashboard():
    return render_template('project_dashboard.html')
@bp.route("/lessons", methods=['GET', 'POST'])
@login_required
def lessons():
    lessons = Lesson.query.all()
    return render_template('lessons.html', lessons=lessons)
@bp.route("/create_lesson", methods=['GET', 'POST'])
@login_required
def create_lesson():
    form = CreateLessonForm()
    quizzes = Quiz.query.all()


    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            description=form.description.data,
            content=form.content.data,
            creator_id=current_user.id,
        )
        db.session.add(lesson)
        db.session.commit()
        flash('Lesson added successfully!', 'success')
        return redirect(url_for('main.lessons'))
    return render_template('create_lesson.html', form=form, quizzes=quizzes)
@bp.route("/lesson/<int:lesson_id>/create_quiz", methods=['GET', 'POST'])
@login_required
def create_quiz(lesson_id):
    form = CreateQuizForm()
    lesson = Lesson.query.get_or_404(lesson_id)

    print(request.method)  # Debug print to check the request method
    print(request.form)  # Debug print to check form data

    if form.validate_on_submit():
        print('submit button oke')  # Debug print for successful form submission

        questions = []
        for question_form in form.questions.entries:
            question_data = {
                'text': question_form.data['question_text'],
                'type': question_form.data['question_type'],
                'options': question_form.data['options'] if question_form.data['question_type'] == 'mcq' else None,
            }
            questions.append(question_data)

        quiz = Quiz(
            title=form.title.data,
            questions=questions,
            lesson_id=lesson_id,
        )
        db.session.add(quiz)
        db.session.commit()

        flash('Quiz added successfully!', 'success')
        return redirect(url_for('main.lesson', lesson_id=lesson_id))

    # Render the form for GET requests or if form validation fails
    return render_template('create_quiz.html', form=form, lesson=lesson, lesson_id=lesson_id)

@bp.route("/lesson/<int:lesson_id>", methods=['GET'])
@login_required
def lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    content_with_quizzes = parse_content_with_markdown(lesson.content, lesson_id)
    return render_template('lesson.html', lesson=lesson, content=content_with_quizzes)
@bp.route("/lesson/<int:lesson_id>/submit_homework", methods=['POST'])
@login_required
def submit_homework(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    homework = Homework.query.filter_by(lesson_id=lesson_id).first()

    if homework:
        submission_content = request.form['homework_submission']
        submission = HomeworkSubmission(
            submission_content=submission_content,
            submitted_by_id=current_user.id,
            homework_id=homework.id
        )
        db.session.add(submission)
        db.session.commit()
        flash('Homework submitted successfully!', 'success')
        return redirect(url_for('main.lesson', lesson_id=lesson_id))
@bp.route("/lesson/<int:lesson_id>/submit_test", methods=['POST'])
@login_required
def submit_test(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    test = Test.query.filter_by(lesson_id=lesson_id).first()

    if test:
        anwsers = request.form['test_anwsers']
        submission = TestSubmission(
            anwsers=anwsers,
            submitted_by_id=current_user.id,
            test_id=test.id
        )
        db.session.add(submission)
        db.session.commit()
        flash('Test submitted successfully!', 'success')
    return redirect(url_for('main.lesson', lesson_id=lesson_id))



def parse_content_with_markdown(content, lesson_id):
    parts = content.split('```')  # Split by markdown markers
    for i in range(len(parts)):
        if i % 2 == 1:  # Every odd part is markdown
            parts[i] = markdown(parts[i])

    # Reassemble and replace quiz placeholders
    content_with_quiz = ''.join(parts)
    quizzes = Quiz.query.filter_by(lesson_id=lesson_id).all()
    for quiz in quizzes:
        quiz_placeholder = f'{quiz.id}'
        content_with_quiz = content_with_quiz.replace(f'{quiz_placeholder}', render_quiz_form(quiz))

    return content_with_quiz
def render_quiz_form(quiz):
    return render_template('quiz_form.html', quiz=quiz)

@login_required
@bp.route('/Test_results', methods=['GET', 'POST'])
def test_results():
    form = TestResultForm()
    if form.validate_on_submit():
        print('submit button oke')
        result = TestSubmission(
            user_id = form.user_id.data,
            test_id = form.Test_id.data,
            score = form.score.data,
            comments = form.comments.data
        )
        db.session.add(result)
        db.session.commit()
        flash('Test results added successfully!', 'success')
        return redirect(url_for('main.view_homework_results'))
    return render_template('Test_Results.html', form=form)
@login_required
@bp.route('/view_homework_results')
def view_homework_results():
    results = TestSubmission.query.all()  # Haal alle huiswerkresultaten op
    print(results)
    # Voorbeeld van het ophalen van de student- en huiswerkinformatie
    formatted_results = []
    for result in results:
        student = User.query.get(result.user_id)  # Haal de naam van de student op
        print(student, student.name)
        homework = Test.query.get(result.test_id)  # Haal de huiswerkdetails op
        print(homework)
        formatted_results.append({
            'student_name': student.name,  # Veronderstelt dat 'name' een attribuut van User is
            'homework_id': homework.id,
            'score': result.score,
            'comments': result.comments,
        })
        print(formatted_results)

    return render_template('view_test_results.html', results=formatted_results)


