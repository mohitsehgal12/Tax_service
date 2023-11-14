import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

conn = sqlite3.connect('tax.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tax (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        calculated_tax REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

conn.commit()
conn.close()

tax_records = {}


@app.route('/tax', methods=['GET'])
def calculate_tax():
    data = request.args
    user_id = data.get('user_id')
    calculated_tax = calculate_tax_logic()

    if calculated_tax is not None:
        conn = sqlite3.connect('tax.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO tax (user_id, calculated_tax) VALUES (?, ?)", (user_id, calculated_tax))
        conn.commit()

        conn.close()

        return jsonify({"calculated_tax": calculated_tax}), 200
    else:
        return "Failed to calculate tax", 400


def calculate_tax_logic():
    return 1000.00


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
