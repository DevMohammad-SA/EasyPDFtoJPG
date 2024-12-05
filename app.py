import os
import sqlite3

from flask import Flask, render_template, request, send_from_directory
from pdf2image import convert_from_path

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/static/outputs/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


@app.route('/submit', methods=['POST'])
def proccess_contacts():
    if request.method == 'POST':
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        contact_message = request.form['contact_message']
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
        print(f"Name: {contact_name}")
        print(f"Email: {contact_email}")
        print(f"Message: {contact_message}")

        print("Button clicked")
        return render_template('submit.html')


if __name__ == '__main__':
    app.run(debug=False)
