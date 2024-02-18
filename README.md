# Library Management System README

## Overview
This is a simple Library Management System implemented using Flask, MySQL, and scikit-learn for book recommendations. The system allows users to log in, sign up, view a list of books, get genre-based book suggestions, add new books, and delete existing books.

## Requirements
- Python 3.x
- Flask
- Flask-MySQLdb
- pandas
- scikit-learn

## Installation
1. Clone the repository: `git clone https://github.com/dhanush1109/Library_Database.git'
2. Navigate to the project directory: `cd library-management-system`
3. Install the required packages: `pip install -r requirements.txt`

## Usage
- Run the application: `python app.py`
- Open a web browser and go to `http://localhost:5000` to access the Library Management System.


## Database Setup
- The system uses a MySQL database. Update the `app.config` in `app.py` with your MySQL database details (host, user, password, and database).

## Features
1. **Login and Signup:**
   - Users can log in with a valid username and password.
   - New users can sign up by providing a username and password.

2. **Book Listing:**
   - View a list of available books with details like title, author, genre, subgenre, height, publisher, and ratings.

3. **Book Suggestions:**
   - Users can receive book suggestions based on their selected genre.
   - Implemented using TF-IDF vectorization and cosine similarity.

4. **Add Book:**
   - Admin users can add new books to the library.

5. **Delete Book:**
   - Admin users can delete existing books from the library.

## How to Run
1. Ensure that the database is set up and running.
2. Run the application: `python app.py`
3. Open a web browser and go to `http://localhost:5000`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries or issues, please contact Dhanush Devadiga at dhanushdevadiga1109@gmail.com.

