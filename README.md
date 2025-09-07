

<img width="1248" height="832" alt="Gemini_Generated_Image_xftyxpxftyxpxfty" src="https://github.com/user-attachments/assets/59013c53-33f8-4e7b-acef-a7169fe28310" />




Work Nest: Project Overview & Application Flow
Work Nest is a full-stack task management application designed with a powerful, hierarchy-based permission system. It allows organizations to control who can assign tasks based on their role and level within the company.

Core Technologies
Backend: Django & Django REST Framework (Python)

Frontend: React (JavaScript, running in a single HTML file)

Database: SQLite (for development), PostgreSQL (for production)

Deployment: Azure App Service & Azure Static Web Apps

API Endpoints & Functionality
The backend provides a secure REST API for all frontend operations. All endpoints (except for login) require a valid JWT Bearer Token for authorization.

Authentication
POST /api/token/

Functionality: User login. Takes username and password in the request body.

Response: Returns a short-lived access token and a long-lived refresh token upon success.

POST /api/token/refresh/

Functionality: Refreshes an expired access token. Takes the refresh token in the body.

Response: Returns a new access token.

Users
GET /api/users/

Functionality: Retrieves a list of all users in the system, including their id, username, and designation_level. This is used by the frontend to populate the "Assign To" dropdown.

Tasks
GET /api/tasks/

Functionality: Retrieves a list of all tasks.

POST /api/tasks/

Functionality: Creates a new task. This endpoint contains the core business logic, checking the creator's permissions (can_assign) and their hierarchical level before allowing the task to be saved.

Permissions
GET /api/permissions/

Functionality: Retrieves a list of all permission rules. Can be used for administrative purposes or to dynamically show/hide UI elements based on a user's role.

Core Concept: The Permission System
The entire application is built around a flexible and secure permission model. It works on two simple principles:

Designation Level: Every user has a number (designation_level) that represents their rank (e.g., CEO = 20, Manager = 15, Intern = 1).

Permission Rules: A separate Permission table in the database acts as a rulebook. For each designation_level, you can set two key flags:

can_assign: Can this role assign tasks to people at a lower level?

can_assign_to_same_level: Can this role assign tasks to people at the same level?

When a user tries to create a task, the backend API acts as a security guard, checking these rules before allowing the task to be created.

Application Flow Diagram
This diagram shows the complete journey from a user logging in to creating a new task, and how the frontend and backend systems interact.

A Note on the "Failed to fetch" Error: The error you highlighted in your screenshot occurs at the very beginning of this flow, on the first arrow moving from the Frontend (React) to the Backend (Django). It means the browser was unable to get any response from the API server, usually because the server isn't running or a network/CORS issue is blocking the connection.

Step-by-Step Flow Explanation
User Login:

The user opens the React application and sees the Login Page.

They enter their username and password.

The React frontend sends a POST request to the Django API's /api/token/ endpoint.

Django verifies the credentials. If correct, it generates a secure JWT Access Token and sends it back.

Viewing the Dashboard:

The React app receives the token and saves it in the browser's session storage. This marks the user as "logged in."

The app now displays the Task Dashboard.

To show the list of tasks, React sends a GET request to /api/tasks/, including the saved token in the Authorization header.

The Django API validates the token, retrieves all tasks from the database, and sends them back as JSON data.

React displays the tasks on the screen.

Creating a New Task (The Logic Check):

The user clicks the "+ Add Task" button, opening a modal.

The user fills in the task title, description, and selects another user to assign the task to from a dropdown.

When they click "Create Task," React sends a POST request to /api/tasks/, again including the token and the new task data.

This is the most critical step: The Django API receives the request. It validates the token and then performs the business logic checks:

Gate 1: Does the logged-in user's role have can_assign set to True?

Gate 2: Is the logged-in user's designation_level greater than the level of the user they are assigning the task to?

If both checks pass, the task is saved to the database.

If either check fails, the API sends back an error message.

The React app receives the success or error response and updates the user interface accordingly.
