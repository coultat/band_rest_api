import pytest
import sqlite3
from api import create_app

#é como se a funçao estivesse na primeira linha
@pytest.fixture
def rascunhos_client():
    app = create_app('rascunhos.db')
    client = app.test_client()
    yield client


@pytest.fixture
def rascunhos_db():
    conn = sqlite3.connect('rascunhos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bands(id integer primary key autoincrement not null, name text, members integer, birth date, genre text);''')
    yield c
    #c.execute('''DROP TABLE bands''')


def test_bands_post(rascunhos_client, rascunhos_db):
    response = rascunhos_client.post(
    '/bands',
    json={
        "name": "the rolling stones",
        "members": 4,
        "birth": "1962",
        "genre": "rock"
    })
    assert response.status_code == 200
    assert response.json['message'] == "if you are reading this is because something went very well :-)"


def test_bands_get(rascunhos_client, rascunhos_db):
    response = rascunhos_client.get(
    '/bands')
    assert response.status_code == 200
    connection = sqlite3.connect('rascunhos.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM BANDS""")
    connection.commit()
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def test_list_bands(rascunhos_client, rascunhos_db):
    response = rascunhos_client.get('/bands/2')
    assert response.status_code == 200
    assert response.json['message'] == 'é nois'


def test_delete_band_from_list(rascunhos_client, rascunhos_db):
    response = rascunhos_client.delete('/bands/2')
    assert response.status_code == 200
    assert response.json['message'] == 'com passo de formiga e sem vontade'


def test_put_from_band(rascunhos_client, rascunhos_db):
    response = rascunhos_client.put(
        '/bands/4',
        json={
            "name": "Soundgarden",
            "members": 4,
            "birth": "1984",
            "genre": "grunge"
        })
    assert response.status_code == 200
    assert response.json['message'] == 'vai forte meu!'


def test_status(rascunhos_client):
    response = rascunhos_client.get('/status')
    assert response.status_code == 200
    assert response.json['message'] == 'ok'


def test_respuesta(rascunhos_client):
    texto = 'qué elegancia la de Francia'
    response = rascunhos_client.post('/resp', json={'mensaje': texto})
    assert response.status_code == 200
    assert response.json['mensaje'] == texto


def test_can_save_band_to_db(rascunhos_client, rascunhos_db):
    response = rascunhos_client.post(
        '/bands',
        json={
            "name": "soulfly",
            "members": 4,
            "birth": '1997',
            "genre": "death_metal"
        })
    assert response.status_code == 200
    connection = sqlite3.connect('rascunhos.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT *
                    FROM bands
                    WHERE name = "soulfly"''')
    row = cursor.fetchall()


def test_testando_coisas_com_o_put(rascunhos_client, rascunhos_db):
    response = rascunhos_client.put(
        '/putz',
        json={
            "name": "Capital Inicial",
            "members": 4,
            "birth": "1987",
            "genre": "mpb"
        })



def test_post_band(rascunhos_client, rascunhos_db):
    response = rascunhos_client.post(
        '/band',
        json={
            "name": "Paralamas do Sucesso",
            "members": 3,
            "birth": "1980",
            "genre": "boiola"
        }
    )
    assert response.status_code == 200
    assert response.json['name'] == "Paralamas do Sucesso"
    assert response.json.get('id') is not None



    #assert response.status_code == 200
    #connection = sqlite3.connect('rascunhos.db')
    #cursor = connection.cursor()
    #cursor.execute('''UPDATE bands SET name = "Capital Inicial", members = 4, birth = "1982", genre = "mpb"
     #               WHERE name = "soulfly" ''')
    #assert response.json['message'] == 'es Belo, es Forte, Impávido Colosso'
