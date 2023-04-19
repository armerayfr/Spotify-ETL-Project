import sqlalchemy
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"


def get_datas():
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
        SELECT * FROM my_played_tracks
    """

    res = cursor.execute(sql_query).fetchall()
    print('res--------', res)