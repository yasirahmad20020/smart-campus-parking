from flask import Flask, render_template, request
import sqlite3
from plate_detector import detect_plate
from database import init_db
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    plate = slot = None

    if request.method == "POST":
        file = request.files["image"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        plate = detect_plate(path)

        conn = sqlite3.connect("parking.db")
        c = conn.cursor()

        c.execute("SELECT slot_id FROM parking_slots WHERE is_available=1 LIMIT 1")
        slot = c.fetchone()[0]

        c.execute("UPDATE parking_slots SET is_available=0 WHERE slot_id=?", (slot,))
        c.execute("INSERT INTO vehicles VALUES (?, ?, ?)",
                  (plate, slot, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        conn.close()

    return render_template("index.html", plate=plate, slot=slot)

app.run(debug=True)
