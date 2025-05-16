# Flask URL Shortener

This project is a web application built with Python and the Flask framework that allows users to shorten long URLs. It uses SQLAlchemy with a SQLite database (`shortener.db`) to store the mappings between short codes and original URLs.

## Features

* Shorten long URLs into unique short codes.
* Redirect users from a short code URL to the original long URL.
* Uses SQLite database to persist URL mappings.
* Includes a mechanism to generate short codes.

## Technologies Used

* Python
* Flask
* SQLAlchemy
* SQLite
* `os` (Python standard library)
* `request` (Flask)
* `redirect` (Flask)
* `url_for` (Flask)
* `render_template` (Flask)
* `abort` (Werkzeug, used by Flask)
* HTML

## Setup and Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Tasfiul/url-shortener
    ```
2.  Navigate to the project directory:
    ```bash
    cd url-shortener
    ```
3.  Create a virtual environment (recommended) and activate it:
    ```bash
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```
4.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Set up the database:
    # Database and tables will be automatically generated when the application is run.

## How to Run

1.  Make sure your virtual environment is activated.
2.  Set the `FLASK_APP` environment variable to point to your application instance :
    ```powershell
    # On Windows (PowerShell)
    $env:FLASK_APP = "hello_app.webapp:app"
    ```
3.  Run the Flask application:
    ```bash
    flask run
    ```
    The URL shortener will be available at `http://127.0.0.1:5000/`.

## Routes

* **GET /** and **POST /** : Handles displaying the form to shorten a URL and processing the form submission.
* **GET /<short_code>** : Redirects the user to the original long URL associated with the provided short code.
