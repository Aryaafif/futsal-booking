from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# koneksi database
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# halaman utama (lihat jadwal + data booking)
@app.route("/")
def index():
    db = get_db()
    data = db.execute("SELECT * FROM booking").fetchall()
    return render_template("index.html", data=data)

# proses booking
@app.route("/booking", methods=["POST"])
def booking():
    nama = request.form["nama"]
    tanggal = request.form["tanggal"]
    jam = request.form["jam"]

    db = get_db()
    db.execute(
        "INSERT INTO booking (nama, tanggal, jam, status) VALUES (?, ?, ?, ?)",
        (nama, tanggal, jam, "Pending")
    )
    db.commit()

    return redirect("/")

# konfirmasi oleh admin
@app.route("/konfirmasi/<int:id>")
def konfirmasi(id):
    db = get_db()
    db.execute("UPDATE booking SET status='Sukses' WHERE id=?", (id,))
    db.commit()
    return redirect("/")

# hapus booking (opsional admin)
@app.route("/hapus/<int:id>")
def hapus(id):
    db = get_db()
    db.execute("DELETE FROM booking WHERE id=?", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)