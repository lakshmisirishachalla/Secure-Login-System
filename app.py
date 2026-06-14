from flask import Flask, request, session, redirect, render_template_string
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"
bcrypt = Bcrypt(app)

conn = sqlite3.connect("users.db")
conn.execute("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE,password TEXT)")
conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u, p = request.form["u"], request.form["p"]
        conn = sqlite3.connect("users.db")
        user = conn.execute("SELECT * FROM users WHERE username=?", (u,)).fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[1], p):
            session["user"] = u
            return redirect("/dashboard")

        return "Invalid Login"

    return render_template_string('''
    <h2>Login</h2>
    <form method="post">
    <input name="u" placeholder="Username"><br><br>
    <input name="p" type="password" placeholder="Password"><br><br>
    <button>Login</button>
    </form>
    <a href="/register">Register</a>
    ''')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u, p = request.form["u"], request.form["p"]
        h = bcrypt.generate_password_hash(p).decode()

        try:
            conn = sqlite3.connect("users.db")
            conn.execute("INSERT INTO users VALUES(?,?)", (u, h))
            conn.commit()
            conn.close()
            return redirect("/")
        except:
            return "User Already Exists"

    return render_template_string('''
    <h2>Register</h2>
    <form method="post">
    <input name="u" placeholder="Username"><br><br>
    <input name="p" type="password" placeholder="Password"><br><br>
    <button>Register</button>
    </form>
    ''')

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return f"<h1>Welcome {session['user']}</h1><a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

app.run(debug=True)