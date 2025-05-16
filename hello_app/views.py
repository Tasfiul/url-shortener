from flask import Flask, request, redirect, url_for, render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os

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
    short_url = None # 

    if request.method == 'POST':
        long_url = request.form['long_url'] # Get the long URL from the form

        
        if not long_url:
            # Handle error if no URL is provided
            return render_template('index.html')

        # Create a new URLMapping object with the long_url
        new_mapping = URLMapping(long_url=long_url, short_code="") # short_code is empty for now

        try:
            db.session.add(new_mapping)
            db.session.commit()

            # Access the ID that was assigned after the commit
            generated_code = generate_short_code(new_mapping.id)

            # --- Update the database entry with the generated short code ---
            new_mapping.short_code = generated_code

            # Commit the session again to save the short code
            db.session.commit()


            short_url = url_for('redirect_to_long_url', short_code=generated_code, _external=True)

        except Exception as e:
            # Handle potential errors
            print(f"Error creating short URL: {e}")
            return render_template('index.html')

    return render_template('index.html', short_url=short_url)

# Route to handle short codes and redirect
@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()

    # If no mapping was found for that short code, return a 404 error
    if not url_mapping:
        abort(404)

    return redirect(url_mapping.long_url)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)