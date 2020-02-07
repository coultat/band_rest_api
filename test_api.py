import pytest
import sqlite3
from api import create_app

#é como se a funçao estivesse na primeira linha
@pytest.fixture
def client():
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


def test_bands_post(client, rascunhos_db):
    response = client.post(
    '/bands',
    json={
        "name": "the rolling stones",
        "members": 4,
        "birth": "1962",
        "genre": "rock"
    })
    assert response.status_code == 200
    assert response.json['message'] == "if you are reading this is because something went very well :-)"


def test_bands_get(client, rascunhos_db):
    response = client.get(
    '/bands')
    assert response.status_code == 200
    connection = sqlite3.connect('rascunhos.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM BANDS""")
    connection.commit()
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def test_list_bands(client, rascunhos_db):
    response = client.get('/bands/2')
    assert response.status_code == 200
    assert response.json['message'] == 'é nois'


def test_delete_band_from_list(client, rascunhos_db):
    response = client.delete('/bands/2')
    assert response.status_code == 200
    assert response.json['message'] == 'com passo de formiga e sem vontade'


def test_put_from_band(client, rascunhos_db):
    response = client.put(
        '/bands/4',
        json={
            "name": "Soundgarden",
            "members": 4,
            "birth": "1984",
            "genre": "grunge"
        })
    assert response.status_code == 200
    assert response.json['message'] == 'vai forte meu!'


def test_status(client):
    response = client.get('/status')
    assert response.status_code == 200
    assert response.json['message'] == 'ok'


def test_respuesta(client):
    texto = 'qué elegancia la de Francia'
    response = client.post('/resp', json={'mensaje': texto})
    assert response.status_code == 200
    assert response.json['mensaje'] == texto


def test_can_save_band_to_db(client, rascunhos_db):
    response = client.post(
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


def test_testando_coisas_com_o_put(client, rascunhos_db):
    response = client.put(
        '/putz',
        json={
            "name": "Capital Inicial",
            "members": 4,
            "birth": "1987",
            "genre": "mpb"
        })



def test_post_band(client, rascunhos_db):
    response = client.post(
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
    assert type(response.json.get('id')) == int


def test_put_band(client, rascunhos_db):
    response = client.post(
        '/band',
        json={
            "name": "Ratos do Porao",
            "members": 5,
            "birth": "1982",
            "genre": "punk brasileiro"
        }
    )
    assert response.status_code == 200
    id = response.json.get('id')
    response = client.put(
        '/band/{id}'.format(id=id),
        json={
            "name": "Ratos de Porao",
            "members": 5,
            "birth": "1982",
            "genre": "punk brasileiro"
        }
    )
    assert response.status_code == 200
    assert response.json['id'] == id
    assert response.json['name'] == "Ratos de Porao"


