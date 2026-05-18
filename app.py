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

    if "user" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM servers")
    servers = cur.fetchall()

    total_servers = len(servers)

    production_count = len(
        [s for s in servers if s[3] == "Production"]
    )

    staging_count = len(
        [s for s in servers if s[3] == "Staging"]
    )

    cur.close()
    conn.close()

    return render_template(
        "dashboard.html",
        user=session["user"],
        servers=servers,
        total_servers=total_servers,
        production_count=production_count,
        staging_count=staging_count
    )

@app.route("/add-server", methods=["GET", "POST"])
def add_server():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        hostname = request.form["hostname"]
        ip_address = request.form["ip_address"]
        environment = request.form["environment"]
        role = request.form["role"]
        status = request.form["status"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO servers
            (hostname, ip_address, environment, role, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                hostname,
                ip_address,
                environment,
                role,
                status
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_server.html")

@app.route("/delete-server/<int:id>")
def delete_server(id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM servers WHERE id=%s",
        (id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
