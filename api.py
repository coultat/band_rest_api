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


    @app.route('/bands', methods=['POST', 'GET'])
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
        if request.method == 'GET':
            return jsonify({'message':'if you are reading this is because was asked in the DB'})

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
            return jsonify({'message': 'vai forte meu!'})




    return app

app = create_app


if __name__ == '__main__':
    my_app = create_app('rascunhos.db')
    my_app.run()
