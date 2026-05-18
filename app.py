from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = "devopsprojectsecret"


def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="flaskdb",
        user="postgres",
        password="mypass",
        port=5432
    )


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )

            conn.commit()

        except Exception as e:
            conn.rollback()
            print("REGISTER ERROR:", e)
            return "Internal Server Error", 500

        finally:
            cur.close()
            conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT * FROM users WHERE email=%s AND password=%s",
                (email, password)
            )

            user = cur.fetchone()

        finally:
            cur.close()
            conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" in session:
        return render_template("dashboard.html", user=session["user"])

    return redirect("/login")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
