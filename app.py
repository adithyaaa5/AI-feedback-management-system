from flask import Flask, render_template, request,redirect,session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret123'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR PASSWORD",   # change this
    database="feedback_db"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    if name == "" or email == "" or message == "":
        return render_template('index.html', error="All fields are required!")

    query = "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)"
    values = (name, email, message)

    cursor.execute(query, values)
    db.commit()

    return render_template('index.html', success="Feedback submitted successfully!")

@app.route('/delete/<int:id>')
def delete(id):
    query = "DELETE FROM feedback WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    return redirect('/admin')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect('/login')

    search = request.args.get('search')

    if search:
        query = "SELECT * FROM feedback WHERE name LIKE %s OR email LIKE %s"
        values = (f"%{search}%", f"%{search}%")
        cursor.execute(query, values)
    else:
        cursor.execute("SELECT * FROM feedback")

    data = cursor.fetchall()
    return render_template('admin.html', feedbacks=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # simple login (hardcoded)
        if username == 'admin' and password == '1234':
            session['logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)