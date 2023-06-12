'''

    Tema            :   Data Restaurant
    Anggota Kelompok:
    1. Aji Nur Cahyo    ( 212102001 )
    2. Dika Nur Handoko ( 212102004 )
    3. M Afda Kurniawan ( 212102010 )

'''

import sqlite3
from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = 'user1234'
basic_auth = BasicAuth(app)

conn = sqlite3.connect('restaurant.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS restaurants
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            alamat TEXT NOT NULL,
            telepon TEXT NOT NULL,
            menu TEXT NOT NULL,
            rating REAL NOT NULL)''')

conn.commit()
conn.close()

@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.json

    if isinstance(data, list):
        conn = sqlite3.connect('restaurant.db')
        c = conn.cursor()

        for item in data:
            nama = item['nama']
            alamat = item['alamat']
            telepon = item['telepon']
            menu = ', '.join(item['menu'])
            rating = item['rating']

            c.execute("INSERT INTO restaurants (nama, alamat, telepon, menu, rating) VALUES (?, ?, ?, ?, ?)",
                    (nama, alamat, telepon, menu, rating))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Data restoran berhasil ditambahkan'}), 201
    else:
        return jsonify({'message': 'Data yang diterima harus berupa array JSON'}), 400

@app.route('/restaurants', methods=['GET'])
@basic_auth.required
def get_all_restaurants():
    
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()

    c.execute("SELECT * FROM restaurants")
    restaurants = c.fetchall()

    response = []
    for restaurant in restaurants:
        data = {
            'id': restaurant[0],
            'nama': restaurant[1],
            'alamat': restaurant[2],
            'telepon': restaurant[3],
            'menu': restaurant[4].split(', '),
            'rating': restaurant[5]
        }
        response.append(data)

    conn.close()
    return jsonify(response)

@app.route('/restaurants/<int:id>', methods=['GET'])
@basic_auth.required
def get_restaurant(id):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM restaurants WHERE id=?", (id,))
    restaurant = c.fetchone()
    
    if restaurant:
        response = {
            'id': restaurant[0],
            'nama': restaurant[1],
            'alamat': restaurant[2],
            'telepon': restaurant[3],
            'menu': restaurant[4].split(', '),
            'rating': restaurant[5]
        }
        return jsonify(response)
    else:
        return jsonify({'message': 'Data restoran tidak ditemukan'}), 404
    
    conn.close()

@app.route('/restaurants/<int:id>', methods=['PUT'])
@basic_auth.required
def update_restaurant(id):
    data = request.json
    
    nama = data['nama']
    alamat = data['alamat']
    telepon = data['telepon']
    menu = ', '.join(data['menu'])
    rating = data['rating']
    
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    c.execute("UPDATE restaurants SET nama=?, alamat=?, telepon=?, menu=?, rating=? WHERE id=?",
            (nama, alamat, telepon, menu, rating, id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Data restoran berhasil diperbarui'}), 200

@app.route('/restaurants/<int:id>', methods=['DELETE'])
@basic_auth.required
def delete_restaurant(id):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    c.execute("DELETE FROM restaurants WHERE id=?", (id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Data restoran berhasil dihapus'}), 200

if __name__ == '__main__':
    app.run(debug=True)
