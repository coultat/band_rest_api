import sqlite3

db_filename = 'rascunhos.db'

conn = sqlite3.connect(db_filename)

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS bands(
        id integer primary key autoincrement not null, 
        name text, 
        members integer, 
        birth date, 
        genre text
    );
    """
)