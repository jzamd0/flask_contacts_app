from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3

app = Flask(__name__)

# SQLite Connection
DATABASE = 'db.sqlite3'

# Settings
app.secret_key = "mysecretkey"

# Routes
@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM contact")
    data = cur.fetchall()
    conn.close()
    return render_template("index.html", contacts = data)

@app.route("/add_contact", methods=["POST"])
def add_contact():
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO contact (fullname, phone, email) VALUES (?, ?, ?)",
            (fullname, phone, email))
        conn.commit()
        conn.close()
        flash("Contact added successfully.")
        return redirect(url_for("index"))

@app.route("/edit/<id>")
def get_contact(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM contact WHERE id = ?', (id,))
    data = cur.fetchall()
    conn.close()
    return render_template("edit-contact.html", contact = data[0])

@app.route("/update/<id>", methods=["POST"])
def update_contact(id):
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("""
            UPDATE contact
            SET fullname = ?,
                email = ?,
                phone = ?
            WHERE id = ?
        """, (fullname, email, phone, id))
        conn.commit()
        conn.close()
        flash("Contact updated successfully.")
        return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete_contact(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("DELETE FROM contact WHERE id = {0}".format(id))
    conn.commit()
    conn.close()
    flash("Contact removed successfully.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(port=3000, debug=True)
