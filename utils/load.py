import sqlalchemy
import pandas as pd
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"


def load_to_sql(df: pd.DataFrame):
    """
    Function to load data to SQL
    """
    print('loading data running.......................')
    print(df)

    # loading database
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    # SQL to create table
    sql_query = """
        CREATE TABLE IF NOT EXISTS my_played_tracks(
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            timestamp VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
        )
    """

    cursor.execute(sql_query)
    print("Opened database successfully....")

    # Only append New Data to avoid duplicates
    try:
        df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print('Data already exists in the database')

    conn.close()
    print("Close database successfully")





