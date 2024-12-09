# import required libraries
import os
import sqlite3

from flask import (Flask, make_response, redirect, render_template, request,
                   send_from_directory)
from flask_babel import Babel, _, g, get_locale, gettext, lazy_gettext
from pdf2image import convert_from_path

# create a new Flask web app
app = Flask(__name__)
# initialize Flask-Babel
babel = Babel(app)

# set the folder to store uploaded PDF files
UPLOAD_FOLDER = 'static/uploads'
# set the folder to store generated images
OUTPUT_FOLDER = 'static/outputs'
# configure the app to store uploaded files in the specified folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# configure the app to store generated images in the specified folder
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
# configure the translations folder
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# configure the languages that the app will support
app.config['LANGUAGES'] = ['en', 'ar']

# ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# inject the locale into the template context


@app.context_processor
def inject_locale():
    print(f"=========[{get_locale()}]=========")
    return {'locale': get_locale()}


# get the locale from the browser's preferred language, or from a cookie
def get_locale():
    lang = request.cookies.get('lang')
    print(f"Current cookie language: {lang}")
    if lang in app.config['LANGUAGES']:
        return lang
    return 'en'  # Explicit default


# Initialize Flask-Babel
babel.init_app(app, locale_selector=get_locale)

# Define a route to set the language


@app.route('/set_language/<lang>')
def set_language(lang):
    resp = make_response(redirect(request.referrer or '/'))
    resp.set_cookie('lang', lang, max_age=60*60*24 *
                    30)  # Cookie expires in 30 days
    print(f"Setting language cookie to: {lang}")  # Debug print
    return resp

# Define the main route for the app


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the list of uploaded PDF files
        files = request.files.getlist('pdf_files')
        image_paths = []  # Store all generated image paths

        for file in files:
            if file:
                # Save each PDF file
                pdf_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], file.filename)
                file.save(pdf_path)

                # Convert each PDF to images
                images = convert_from_path(pdf_path)
                for i, image in enumerate(images):
                    image_filename = f"{os.path.splitext(file.filename)[0]}_page_{
                        i + 1}.jpg"
                    image_path = os.path.join(
                        app.config['OUTPUT_FOLDER'], image_filename)
                    image.save(image_path, 'JPEG')
                    image_paths.append(f"outputs/{image_filename}")

        return render_template('result.html', image_paths=image_paths)

    return render_template('home.html')

# Define a route to handle the contact form


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


# Define a route to handle the about page
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


# Define a route to serve the generated images
@app.route('/static/outputs/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


# Define a route to handle the contact form submissions
@app.route('/submit', methods=['POST'])
def proccess_contacts():
    if request.method == 'POST':
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        contact_message = request.form['contact_message']
        print(f"Name: {contact_name}")
        print(f"Email: {contact_email}")
        print(f"Message: {contact_message}")

        try:
            conn = sqlite3.connect('database.db')
            cr = conn.cursor()
            cr.execute(
                "CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT,date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(email))")
            cr.execute("SELECT * FROM contacts WHERE email = ?",
                       (contact_email,))
            existing_contact = cr.fetchone()
            if existing_contact:
                return render_template('dublicate.html')
            else:
                cr.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
                           (contact_name, contact_email, contact_message))
            conn.commit()
            conn.close()
        except conn.IntegrityError:
            print("you already sent a message !")
        print("Button clicked")
        return render_template('submit.html')


if __name__ == '__main__':
    app.run(debug=False)
