from flask import Flask, request, redirect, url_for, render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os
# We'll need other imports later for code generation and maybe forms

from . import app

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shortener.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Model Definition ---
class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    long_url = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<URLMapping {self.short_code} -> {self.long_url}>'

# --- Short Code Generation Function ---
def generate_short_code(id):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)

    short_code = []
    while id > 0:
        remainder = id % base
        short_code.insert(0, characters[remainder])
        id //= base

    if not short_code:
        return characters[0]

    return "".join(short_code)

# --- Routes ---
@app.route('/', methods=['GET', 'POST']) # Listen for both GET and POST
def index():
    short_url = None # Initialize short_url to None

    if request.method == 'POST':
        long_url = request.form['long_url'] # Get the long URL from the form

        # Basic validation (you might want more robust URL validation)
        if not long_url:
            # Handle error if no URL is provided
            # For now, just re-render the form, maybe add an error message later
            return render_template('index.html')

        # --- Create the database entry and get the ID ---
        # Create a new URLMapping object with the long_url
        new_mapping = URLMapping(long_url=long_url, short_code="") # short_code is empty for now

        try:
            # Add the new mapping to the session and commit
            db.session.add(new_mapping)
            db.session.commit() # *** This is crucial - it assigns the unique ID ***

            # --- Generate the short code using the newly assigned ID ---
            # Access the ID that was assigned after the commit
            generated_code = generate_short_code(new_mapping.id)

            # --- Update the database entry with the generated short code ---
            # Assign the generated code to the short_code attribute
            new_mapping.short_code = generated_code

            # Commit the session again to save the short code
            db.session.commit()

            # --- Prepare the short URL to display ---
            # Construct the full short URL (e.g., http://127.0.0.1:5000/abc)
            # In a real app, you'd use your domain name instead of 127.0.0.1:5000
            short_url = url_for('redirect_to_long_url', short_code=generated_code, _external=True)

        except Exception as e:
            # Handle potential errors (e.g., database error, validation error)
            print(f"Error creating short URL: {e}") # Print error to console
            # For now, just re-render the form, maybe add an error message later
            return render_template('index.html')


    # Render the index.html template
    # On GET, short_url will be None, so the {% if short_url %} block is skipped
    # On POST (successful), short_url will be set, and the block is rendered
    return render_template('index.html', short_url=short_url)

# New: Route to handle short codes and redirect
# The <short_code> part captures the code from the URL
@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    # Find the URL mapping with the matching short code in the database
    # .filter_by() allows filtering by column values
    # .first() gets the first result (since short codes are unique, there should be at most one)
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()

    # If no mapping was found for that short code, return a 404 error
    if not url_mapping:
        abort(404)

    # If a mapping was found, redirect the user to the original long URL
    # redirect() is a Flask function for performing HTTP redirects
    return redirect(url_mapping.long_url)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)