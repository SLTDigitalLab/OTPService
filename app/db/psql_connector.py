#! /usr/bin/python
from configparser import ConfigParser
import psycopg2
import psycopg2.extras


def default_config(filename="db/database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db


def version():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = default_config()

        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print("PostgreSQL database version:")
        cur.execute("SELECT version()")

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


class DB:
    conn = None
    cursor = None

    def __init__(self, params, cf=psycopg2.extras.RealDictCursor) -> None:
        self.conn = psycopg2.connect(**params)
        self.cursor = self.conn.cursor(cursor_factory=cf)

    def get_conn(self):
        return self.conn

    def get_cur(self):
        return self.cursor

    def commit(self):
        self.conn.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, size):
        return self.cursor.fetchmany(size)

    def fetchall(self):
        return self.cursor.fetchall()

    def cur(self):
        self.cursor = self.conn.cursor()

    def exec(self, query: str, vars: tuple = None):
        return self.cursor.execute(query, vars)

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def __del__(self):
        self.close()
