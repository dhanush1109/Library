from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'yourusername'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'yourdatabasename'

db = MySQL(app)

class Book:
    def __init__(self, book_id, title, author, genre, subgenre, height, publisher, ratings):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.subgenre = subgenre
        self.height = height
        self.publisher = publisher
        self.ratings = ratings
        
class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user_data = cursor.fetchone()

        if user_data:
            user = User(*user_data)
            # You may want to implement a session or another authentication mechanism here
            return redirect('/book_details')
        else:
            error_message = "Invalid username or password. Please try again."

        return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.connection.commit()

        return redirect('/')

    return render_template('signup.html')

@app.route('/book_details')
def homepage():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    books = [Book(*row) for row in data]

    return render_template('book_details.html', books=books)

@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    if request.method == 'POST':
        user_genre = request.form['genre']

        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()

        vectorizer = TfidfVectorizer(stop_words='english')
        text_columns = ['Title', 'Author', 'Genre', 'SubGenre']
        text_data = pd.DataFrame(data)
        text_data = text_data.fillna('').astype(str).apply(lambda x: ' '.join(x), axis=1)
        text_vectors = vectorizer.fit_transform(text_data)

        def get_genre_suggestions(selected_genre):
            genre_vector = vectorizer.transform([selected_genre])
            cosine_similarities = linear_kernel(genre_vector, text_vectors).flatten()
            related_books_indices = cosine_similarities.argsort()[:-6:-1]
            suggestions = [data[i][1] for i in related_books_indices]  # Assuming the title is in the second column
            return suggestions

        selected_genre = user_genre  # Use the user's selected genre
        suggestions = get_genre_suggestions(selected_genre)
        print(f"Suggested books for {selected_genre} genre:")
        print(suggestions)

        return render_template('suggestion.html', user_genre=user_genre, suggested_books=suggestions)

    return render_template('suggestion.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        subgenre = request.form['subgenre']
        height = request.form['height']
        publisher = request.form['publisher']
        ratings = request.form['ratings']

        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO books (Title, Author, Genre, SubGenre, Height, Publisher, Ratings) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (title, author, genre, subgenre, height, publisher, ratings))
        db.connection.commit()

        return redirect('/book_details')

    return render_template('add_book.html')



@app.route('/delete_book', methods=['GET', 'POST'])
def delete_book():
    if request.method == 'POST':
        book_id_to_delete = request.form['book_id']

        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM books WHERE Book_ID = %s", (book_id_to_delete,))
        db.connection.commit()

        return redirect('/book_details')
    
    return render_template('delete_book.html')

if __name__ == '__main__':
    app.run(debug=True)
