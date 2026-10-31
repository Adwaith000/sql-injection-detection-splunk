from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

DB = "users.db"

def get_db():
    return sqlite3.connect(DB)

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")

        # INTENTIONALLY VULNERABLE — LAB ONLY.
        # Do not expose this application to the public internet.
        q = f"SELECT * FROM users WHERE username='{u}' AND password='{p}'"

        db = get_db()
        try:
            result = db.execute(q).fetchone()
        except sqlite3.Error:
            result = None
        finally:
            db.close()

        with open("flask.log", "a", encoding="utf-8") as log:
            log.write(f"USER={u} PASS={p}\n")

        if result:
            return render_template("dashboard.html")

        message = "Login failed"

    return render_template("login.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
