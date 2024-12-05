# PDF to Image Converter Flask App

This is a Flask web application that allows users to upload PDF files and convert each page into JPEG images.
It also includes basic pages such as "About" and "Contact," with a contact form that stores submissions in an SQLite database.

## Features

- Upload multiple PDF files and convert them into images.
- View and download the converted images.
- Contact form with data storage using SQLite.
- Includes "Home," "About," "Contact," and result pages.

## Project Structure

.├── static/ │ ├── outputs/ # Folder for storing converted images │ └── uploads/ # Folder for storing uploaded PDF files ├── templates/ # HTML templates for the web pages │ ├── about.html │ ├── base.html │ ├── contact.html │ ├── duplicate.html │ ├── home.html │ ├── result.html │ └── submit.html ├── .gitignore # Specifies files/folders to be ignored by Git ├── app.py # Main Flask application file ├── database.db # SQLite database for contact form submissions └── requirements.txt # List of Python dependencies

## Prerequisites

Ensure the following are installed:

- Python 3.x
- Flask
- pdf2image library
- SQLite

## Installation

1. **Clone the repository:**
   git clone <https://github.com/DevMohammad-SA/EasyPDFtoJPG>
   cd [repository-directory]

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure directories for uploads and outputs:**

   ```bash
   mkdir -p static/uploads static/outputs
   ```

## Usage

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

2. **Open the application in your browser:**

   <http://127.0.0.1:5000/>

### Routes

- `/` - Home page for uploading PDFs.
- `/about` - About page.
- `/contact` - Contact form page.
- `/submit` - Handles contact form submissions.
- `/static/outputs/<filename>` - Serves converted images.

## Database Schema

The `contacts` table in `database.db` stores contact form submissions:

```sql
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    message TEXT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## .gitignore

The `.gitignore` file should exclude the following:

```txt
.DS_Store
*.pyc
__pycache__/
instance/
.env
database.db
static/uploads/
static/outputs/
```

## License

This project is open-source. Feel free to modify and distribute it.

```md
### Notes:

1. Replace `<repository-url>` with the actual GitHub repository URL if applicable.
2. The `.gitignore` section ensures temporary files and sensitive data are excluded.
3. You can modify the "License" section based on your preferred license type.
```
