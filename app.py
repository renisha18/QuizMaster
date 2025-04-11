from flask import Flask, render_template, request, redirect
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

# Function to reconnect DB if needed
def get_db_connection():
    if not db.is_connected():
        db.reconnect()
    return db

# ------------------ Home/User Registration ------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    name = ""
    email = ""
    role = ""

    if request.method == 'POST':
        userdetails = request.form
        name = userdetails['username']
        email = userdetails['email']
        role = userdetails['role']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                return "⚠️ This email is already registered!"

            cursor.execute("INSERT INTO users (username, email, role) VALUES (%s, %s, %s)", (name, email, role))
            conn.commit()
            cursor.close()
            if role == 'teacher':
                return redirect('/main')
            elif role == 'student':
                return redirect('/quiz')

        except Exception as e:
            return f"Failed to add user: {e}"

    return render_template('index.html', name=name, email=email, role=role)

# ------------------ Load Question Form ------------------

@app.route('/main')
def main():
    return render_template('questions_form.html')

# ------------------ Submit Questions ------------------

@app.route('/submit_questions', methods=['POST'])
def submit_questions():
    for i in range(1, 6):  # 5 questions
        question = request.form.get(f'question{i}')
        option1 = request.form.get(f'option1_{i}')
        option2 = request.form.get(f'option2_{i}')
        option3 = request.form.get(f'option3_{i}')
        correct_option = int(request.form.get(f'correct{i}'))

        cursor.execute('''
            INSERT INTO questions (question_text, option1, option2, option3, correct_option)
            VALUES (%s, %s, %s, %s, %s)
        ''', (question, option1, option2, option3, correct_option))

    db.commit()
    return "✅ Questions saved successfully!"

# ------------------ Show Quiz Page ------------------

@app.route('/quiz')
def quiz():
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    return render_template('quiz.html', questions=questions)

# ------------------ Submit Quiz Answers ------------------

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    username = request.form.get('username')
    score = 0

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    for question in questions:
        qid = str(question['id'])
        user_answer = request.form.get(f'question_{qid}')
        if user_answer and int(user_answer) == question['correct_option']:
            score += 10

    cursor.execute("INSERT INTO scores (username, score) VALUES (%s, %s)", (username, score))
    db.commit()

    return render_template('result.html', username=username, score=score)

# ------------------ View Users & Scores ------------------

@app.route('/users')
def users():
    try:
        conn = get_db_connection()

        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM scores")
            users = cursor.fetchall()
            cursor.close()
            return render_template('users.html', users=users)
        else:
            return 'Failed to connect to MySQL.'

    except Exception as e:
        return f"Failed to fetch users: {e}"

# ------------------ Run App ------------------

if __name__ == '__main__':
    app.run(debug=True)