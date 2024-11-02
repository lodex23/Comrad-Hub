# Comrad Hub

Comrad Hub is a collaborative platform designed to facilitate project management, team training, skill assessment, and overall progress tracking. It is tailored to enable users to create, manage, and follow up on projects while providing comprehensive training tools that include lessons, quizzes, and student performance tracking.

## Features

### 1. User Management
- **Secured Registration and Login System**: Users can register with a secure token-based system and log in with password protection.
- **Role-Based Access**: Admins and users have different access levels, ensuring appropriate permissions throughout the platform.

### 2. Project Management
- **Create and Manage Projects**: Users can create projects that are visible to all members and track earnings and progress.
- **Task Assignment**: Assign tasks within projects, set deadlines, and monitor their status.
- **Documents and Notes**: Upload documents related to projects and maintain detailed notes.
- **Issue and Idea Tracking**: Log issues and suggest ideas to improve project outcomes.

### 3. Training System
- **Lesson Creation**: Users can create lessons with text, images, videos, links, and embedded quizzes.
- **Quiz Creation**: Fully customizable quizzes with various question types (string input, multiple choice, yes/no, true/false, textarea).
- **Integrated Lesson Workflow**: Embed quizzes directly within lessons for a seamless training experience.
- **Homework and Tests**: Assign homework and tests, and review them with scoring capabilities.

### 4. Follow-Up System
- **Student Progress Tracking**: Monitor and assess the progress of students through lessons and tests.
- **Performance Review**: Provide detailed feedback and scores for homework and tests, enabling a comprehensive evaluation of student skills.
- **Skill and Knowledge Reports**: Generate reports that show individual and group performance metrics over time.

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- PostgreSQL database
- Flask
- Flask extensions (e.g., Flask-SQLAlchemy, Flask-Login, Flask-WTF)
- Node.js (for frontend dependencies if applicable)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/comrad-hub.git
   cd comrad-hub
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database:
   - Create a PostgreSQL database.
   - Update `config.py` with your database URI.
5. Run database migrations:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. Run the application:
   ```bash
   flask run
   ```

## Usage
- Navigate to `http://127.0.0.1:5000` to access the platform.
- Register with a valid token provided by the administrator.
- Create and manage projects, lessons, and track student performance through the provided interfaces.

## Development
### Folder Structure
```
comrad-hub/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   └── templates/
│       └── (HTML templates)
├── migrations/
├── static/
├── config.py
├── run.py
└── README.md
```

### Key Files
- **`app/__init__.py`**: Initializes the app and extensions.
- **`app/models.py`**: Contains all database models for user, project, task, lesson, and quiz structures.
- **`app/routes.py`**: Defines all the routes for handling user requests and interactions.
- **`app/forms.py`**: Contains form definitions for user input.
- **`config.py`**: Configuration file for database and app settings.

## Contribution
We welcome contributions! Please fork the repository and create a pull request with detailed information about the changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Contact
For any questions or support, please reach out to [your email/contact information].

