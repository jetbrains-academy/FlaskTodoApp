# Flask Project & Task Manager

A simple Flask-based web application that allows users to manage projects and their associated tasks. Each project has its own set of tasks, and you can create, update, delete projects and tasks interactively.

---

## Features

- **Projects**
  - Create new projects.
  - View all projects on the homepage.
  - Delete a project along with all associated tasks.
  
- **Tasks**
  - Add tasks to specific projects.
  - Mark tasks as complete or incomplete.
  - Delete individual tasks.

---

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (via SQLAlchemy ORM)
- **Frontend**: HTML, CSS, Jinja2, Bootstrap for styling.

---

## Prerequisites

Ensure you have the following installed on your machine:

- Python 3.7 or higher
- pip (Python package manager)

---

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/project-task-manager.git
    cd project-task-manager
    ```

2. **Create a Virtual Environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate     # On Windows
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Application

1. **Start the Application**

    Run the application in development mode:

    ```bash
    python app.py
    ```

2. **Access the Application**

    Open your browser and navigate to:

    ```
    http://127.0.0.1:5000/
    ```

---

## Usage

### Home Page

The homepage lists all projects. 

- Add a new project using the input form at the top of the page.
- View tasks associated with a project using the "View Tasks" button.
- Delete a project (and all tasks associated with it) using the "Delete Project" button.

### Project Task Management

Inside a specific project’s task page, you can:

- Add tasks using the "Add Task" form.
- Mark tasks as complete or incomplete.
- Delete individual tasks.

A **"Back to Projects"** button is available for easy navigation to the homepage.

```bash
pip install -r requirements.txt
```

---

## Design and Aesthetics

- A **pastel gradient background** gives the application a soft and modern look.
- **Responsive design** is ensured using Bootstrap’s grid system.
- **Interactive user experience**, with hover effects and confirmation prompts for deleting tasks and projects.

---

## Known Issues and Limitations

- No authentication or user access control (all features are open to anyone who uses the app).
- Currently, there’s no pagination for larger lists of projects or tasks.

---

## Future Improvements

- Add user authentication to make projects and tasks user-specific.
- Implement advanced task features, such as deadlines or task priorities.
- Improve database efficiency for handling large datasets.
- Add API endpoints for integration with other systems.

---

## Contribution

Contributions are welcome! If you'd like to report a bug, suggest a feature, or submit improvements:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---


Happy coding!