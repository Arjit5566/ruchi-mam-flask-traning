from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'library_management_system_secret_key_2026'

# Database configuration: using SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name=None, username=None, password=None, **kwargs):
        super().__init__(**kwargs)
        if name is not None: self.name = name
        if username is not None: self.username = username
        if password is not None: self.password = password

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_no = db.Column(db.String(50), nullable=False)
    book_name = db.Column(db.String(150), nullable=False)
    book_author = db.Column(db.String(100), nullable=False)
    book_type = db.Column(db.String(50), nullable=False)
    issue_date = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, book_no=None, book_name=None, book_author=None, book_type=None, issue_date=None, **kwargs):
        super().__init__(**kwargs)
        if book_no is not None: self.book_no = book_no
        if book_name is not None: self.book_name = book_name
        if book_author is not None: self.book_author = book_author
        if book_type is not None: self.book_type = book_type
        if issue_date is not None: self.issue_date = issue_date

# Create tables inside application context
with app.app_context():
    db.create_all()

# Helper function to check login status
def is_logged_in():
    return 'user_id' in session

# Routes

# 1. Home Page with Sign Up and Login buttons
@app.route('/')
def home():
    if is_logged_in():
        return redirect(url_for('dashboard'))
    return render_template('home.html')

# 2. Sign Up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if is_logged_in():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not name or not username or not password:
            flash('Please fill in all fields!', 'danger')
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists! Please choose another.', 'warning')
            return redirect(url_for('signup'))

        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# 3. Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password!', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

# 4. Dashboard (After Login Page) - Contains "See" and "Submit" buttons
@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        flash('Please login to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    total_books = Book.query.count()
    return render_template('dashboard.html', name=session.get('name'), total_books=total_books)

# 5. Submit Book Page (Add Book details)
@app.route('/submit', methods=['GET', 'POST'])
def submit_book():
    if not is_logged_in():
        flash('Please login to submit books.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        book_no = request.form.get('book_no', '').strip()
        book_name = request.form.get('book_name', '').strip()
        book_author = request.form.get('book_author', '').strip()
        book_type = request.form.get('book_type', '').strip()
        issue_date = request.form.get('issue_date', '').strip()

        if not (book_no and book_name and book_author and book_type and issue_date):
            flash('All fields are required!', 'danger')
            return redirect(url_for('submit_book'))

        new_book = Book(
            book_no=book_no,
            book_name=book_name,
            book_author=book_author,
            book_type=book_type,
            issue_date=issue_date
        )
        db.session.add(new_book)
        db.session.commit()

        flash(f'Book "{book_name}" submitted successfully!', 'success')
        return redirect(url_for('see_books'))

    return render_template('submit_book.html')

# 6. See Details Page (View all submitted books)
@app.route('/see')
def see_books():
    if not is_logged_in():
        flash('Please login to see book details.', 'warning')
        return redirect(url_for('login'))

    books = Book.query.order_by(Book.id.desc()).all()
    return render_template('see_books.html', books=books)

# 7. Delete Book Route (Bonus management feature)
@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if not is_logged_in():
        return redirect(url_for('login'))

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f'Book #{book.book_no} deleted successfully.', 'info')
    return redirect(url_for('see_books'))

# 8. Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)