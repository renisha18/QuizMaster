
🧠 Quiz App
A web-based quiz application built with Flask and MySQL, featuring role-based access for teachers and students. Teachers can create quizzes, while students can take them and view scores instantly.

🚀 Features
🔐 User registration & login

👨‍🏫 Role-based access (Teacher & Student)

📝 Teachers can:

Create quiz categories

Add, edit, and delete questions

👨‍🎓 Students can:

Take quizzes

View automatic scores and past results

💾 MySQL database for secure data storage

🖥️ Simple and responsive interface

🛠️ Tech Stack
Frontend: HTML, CSS, Bootstrap

Backend: Python (Flask)

Database: MySQL

📸 Screenshots
(Add screenshots here to showcase UI if available)

🔧 Setup Instructions
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/quiz-app.git
cd quiz-app
Create a virtual environment & install dependencies

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure the database

Set up a MySQL database (e.g., quizdb)

Update database credentials in config.py or app.py

Run the application

bash
Copy
Edit
flask run
Access in browser

arduino
Copy
Edit
http://localhost:5000
📂 Folder Structure
arduino
Copy
Edit
quiz-app/
├── static/
├── templates/
├── app.py
├── config.py
├── requirements.txt
└── README.md
🧑‍💻 Future Enhancements
Timer for quizzes

Question randomization

Export results

Admin dashboard

