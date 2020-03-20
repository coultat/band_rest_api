from flask import Flask, jsonify, request
import sqlite3

def create_app(db_name):
    app = Flask(__name__)

    @app.route('/status', methods=['GET'])
    def status():
        return jsonify({'message': 'ok'})

    @app.route('/resp', methods=['POST'])
    def resp():
        print(request.json)
        return jsonify(request.json)


    @app.route('/bands', methods=['POST'])
    def bands():
        if request.method == 'POST':
            args = request.json
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bands(name, members, birth, genre)VALUES(?,?,?,?)'''
                           ,(args['name'], args['members'], args['birth'], args['genre']),
            )
            conn.commit()
            conn.close()
            return jsonify({'message':'if you are reading this is because something went very well :-)'})


    @app.route("/bands", methods=['GET'])
    def get_list_bands():
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM bands;""")
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({"id": row[0], "name": row[1], "members": row[2], "birth": row[3], "style": row[4]})
        return jsonify({'data': data})

    @app.route('/band', methods=['POST'])
    def post_band():
        args = request.json
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        bands = {
            'name': args['name'],
            'members': args['members'],
            'birth': args['birth'],
            'genre': args['genre']
        }
        cursor.execute('''INSERT INTO bands(name, members, birth, genre) 
                            VALUES(?,?,?,?)'''
                       , (args['name'], args['members'], args['birth'], args['genre']))
        return jsonify({'id': cursor.lastrowid, **bands})

    @app.route('/band/<id>', methods=['PUT'])
    def update_band(id):
        args = request.json
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute('''UPDATE bands SET name = (?), members = (?), birth = (?),genre = (?) 
                        WHERE id = ?''', (args['name'], args['members'], args['birth'], args['genre'], id, ))
        connection.commit()
        return jsonify({'id': int(id), **args})


    @app.route('/band', methods=['PATCH'])
    def patch_band(id = 5):
        args = request.json
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        query =  'UPDATE bands SET'
        i = 0
        for key, value in args.items():
            if i > 0:
                query += ','
            query += ' ' + key + ' = "' + str(value) + '"'
            i += 1
        query += ' WHERE id = ?'
        cursor.execute(query, (id,))
        cursor.execute("""SELECT * FROM bands WHERE id = 5""")
        rows = cursor.fetchone() #rows[1] é o nome da banda
        connection.commit()
        return jsonify({'message': rows[1]})


    @app.route('/bands/<id>', methods=['GET', 'DELETE', 'PUT'])
    def list_bands(id):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if request.method == 'GET':
            cursor.execute('''SELECT * FROM bands WHERE id = ?''', (id,))
            row = cursor.fetchall()
            print(row)
            return jsonify({'message': 'é nois'})
        if request.method == 'DELETE':
            cursor.execute(''' DELETE FROM bands WHERE id = ?''', (id,))
            conn.commit()
            return jsonify({'message': 'com passo de formiga e sem vontade'})
        if request.method == 'PUT':
            args = request.json
            cursor.execute('''UPDATE bands SET name = (?), members = (?), birth = (?),genre = (?) 
                        WHERE id = ?;''', (args['name'], args['members'], args['birth'], args['genre'], name, ))
            conn.commit()



    return app

app = create_app


if __name__ == '__main__':
    my_app = create_app('rascunhos.db')
    #my_app.run()
    my_app.run(host='0.0.0.0')
