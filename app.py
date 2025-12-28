from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "students.db"


def get_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    """)
    conn.commit()
    conn.close()


@app.route("/students", methods=["POST"])
def add_student():
    data = request.json

    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "Invalid data"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)",
        (data["name"], data["age"])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Student added"}), 201


@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    students = []
    for r in rows:
        students.append({
            "id": r[0],
            "name": r[1],
            "age": r[2]
        })

    return jsonify(students)


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.json

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name=?, age=? WHERE id=?",
        (data["name"], data["age"], id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Student updated"})


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted"})

@app.route("/add")
def add_student_browser():
    name = request.args.get("name")
    age = request.args.get("age")

    if not name or not age:
        return "Name and age required"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)",
        (name, int(age))
    )
    conn.commit()
    conn.close()

    return "Student added"

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
