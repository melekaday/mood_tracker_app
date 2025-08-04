from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL bağlantısı
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Melek4334",  # Şifreyi koyduysan buraya yaz
    database="mood_tracker"
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mood = request.form["mood"]
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = db.cursor()
        cursor.execute("INSERT INTO moods (mood, created_at) VALUES (%s, %s)", (mood, date))
        db.commit()
        cursor.close()

        return redirect("/history")

    return render_template("index.html")

@app.route("/history")
def history():
    cursor = db.cursor()
    cursor.execute("SELECT mood, created_at FROM moods ORDER BY created_at DESC")
    moods = cursor.fetchall()
    cursor.close()
    return render_template("history.html", moods=moods)

if __name__ == "__main__":
    app.run(debug=True)
