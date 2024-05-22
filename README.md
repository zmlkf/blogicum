# Blogicum

Blogicum is a website where users can read a feed of posts. It allows user registration, implemented using `django.contrib.auth.forms.UserCreationForm`. Authenticated users can edit their own posts, comment on posts, and delete them.

## Installation

1. Clone the project repository:

   ```bash
   git clone git@github.com:zmlkf/blogicum.git
   ```

2. Navigate to the project directory:

   ```bash
   cd blogicum
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Perform migrations:

   ```bash
   python manage.py migrate
   ```

2. Load initial data into the database:

   ```bash
   python manage.py loaddata db.json
   ```

3. Run the development server:

   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```

4. Access the project locally through [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Technologies Used

- Django: a Python web framework.
- HTML/CSS: markup and styling languages for creating the user interface.
- JavaScript: programming language for interactive elements on web pages.
- SQLite: lightweight relational database used in Django for data storage.
- Git: version control system, used for managing project code and versioning.
- GitHub: platform for hosting projects using the Git version control system.

## Author

Roman Zemliakov ([GitHub](https://github.com/zmlkf))

```