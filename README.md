# Blogicum

Blogicum is a website where users can read a feed of posts. It allows user registration, implemented using `django.contrib.auth.forms.UserCreationForm`. Authenticated users can edit their own posts, comment on posts, and delete them.

## Installation

1. Clone the project repository:

   ```bash
   git clone git@github.com:zmlkf/django_sprint4.git
   ```

2. Navigate to the project directory:

   ```bash
   cd django_sprint4
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

## Author

Roman Zemliakov ([GitHub](https://github.com/zmlkf))

```