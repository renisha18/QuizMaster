from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'renisha18'

# Global DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="klrahulreni1801",
    database="quiz_platform"
)
cursor = db.cursor(dictionary=True)


def get_db_connection():
    if not db.is_connected():
        db.reconnect()
    return db

# ------------------ Home/User Registration ------------------
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "⚠️ Email already registered. Please log in instead."

        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                       (name, email, password, role))
        db.commit()

        session['username'] = name

        if role == 'teacher':
            return redirect('/new_quiz')
        else:
            return redirect('/quiz')

    return render_template('signup.html')


# ------------------ Login ------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (name, password))
        user = cursor.fetchone()

        if user:
            session['username'] = name
            role = user['role']
            if role == 'teacher':
                return redirect('/new_quiz')
            else:
                return redirect('/quiz')
        else:
            return "❌ Incorrect username or password."

    return render_template('login.html')

# ------------------ Teacher: Add New Category ------------------

@app.route('/new_quiz', methods=['GET', 'POST'])
def new_quiz():
    cursor = db.cursor(dictionary=True)

    # Fetch existing quiz categories
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if request.method == 'POST':
        category_name = request.form['category_name']
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
        db.commit()
        return redirect('/new_quiz')  # refresh page after adding new category

    return render_template('new_quiz.html', categories=categories)

@app.route("/add_category", methods=["POST"])
def add_category():
    category_name = request.form["category"]
    cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
    db.commit()
    category_id = cursor.lastrowid
    return redirect(url_for("add_questions", category_id=category_id))


# ------------------ Teacher: Add Questions ------------------

@app.route("/add_questions/<int:category_id>")
def add_questions(category_id):
    cursor.execute("SELECT name FROM categories WHERE id = %s", (category_id,))
    category = cursor.fetchone()
    return render_template("questions_form.html", category_id=category_id, category_name=category["name"])

@app.route("/submit_questions/<int:category_id>", methods=["POST"])
def submit_questions(category_id):
    try:
        for i in range(1, 6):
            question = request.form[f"question{i}"]
            option1 = request.form[f"option1_{i}"]
            option2 = request.form[f"option2_{i}"]
            option3 = request.form[f"option3_{i}"]
            correct = request.form[f"correct_{i}"]

            cursor.execute("""
                INSERT INTO questions (category_id, question_text, option1, option2, option3, correct_option)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (category_id, question, option1, option2, option3, correct))

        db.commit()
        return "✅ Questions saved successfully!"
    
    except Exception as e:
        db.rollback()
        return f"❌ Error saving questions: {str(e)}"

# ------------------ Student: Take Quiz ------------------

@app.route('/quiz')
def quiz():
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    return render_template("quiz_categories.html", categories=categories)

@app.route('/quiz/<int:category_id>')
def show_quiz(category_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions WHERE category_id = %s", (category_id,))
    questions = cursor.fetchall()
    
    # Optional: Fetch category name if you want to show it in the page
    cursor.execute("SELECT name FROM categories WHERE id = %s", (category_id,))
    category = cursor.fetchone()
    
    cursor.close()
    return render_template("quiz.html", questions=questions, category=category,category_id=category_id)

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    username = session.get('username') 
    score = 0
    category_id = request.form.get('category_id')

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    for question in questions:
        qid = str(question['id'])
        user_answer = request.form.get(f'question_{qid}')
        if user_answer and int(user_answer) == question['correct_option']:
            score += 10

    cursor.execute("INSERT INTO scores (username, score, category_id) VALUES (%s, %s, %s)", (username, score, category_id))
    db.commit()

    return render_template('result.html', username=username, score=score)




# ------------------ View Scores and Question Sets ------------------

@app.route('/users')
def users():
    cursor.execute("SELECT * FROM scores")
    users = cursor.fetchall()
    return render_template('users.html', users=users)

@app.route("/question_sets")
def view_question_sets():
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    return render_template("view_question_sets.html", categories=categories)

@app.route("/view_questions/<int:category_id>")
def view_questions_in_category(category_id):
    cursor.execute("SELECT name FROM categories WHERE id = %s", (category_id,))
    category = cursor.fetchone()

    cursor.execute("SELECT * FROM questions WHERE category_id = %s", (category_id,))
    questions = cursor.fetchall()

    cursor.execute("SELECT username, score FROM scores WHERE category_id = %s", (category_id,))
    scores = cursor.fetchall()

    return render_template("view_questions.html", category=category, questions=questions, scores=scores)
# ------------------ Run App ------------------

if __name__ == '__main__':
    app.run(debug=True)