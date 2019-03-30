import sqlite3
import uuid
Q_CREATE_TABLE = """CREATE TABLE content (id text,
                                          img blob,
                                          url text,
                                          title text,
                                          description text)"""
Q_INSERT = "INSERT INTO content VALUES(?, ?, ?, ?, ?)"
Q_SELECT = "SELECT * FROM content WHERE id=?"
Q_SELECT_IMG = "SELECT img FROM content WHERE id=?"


class WebsiteDB:
    def __init__(self, dbname="website.db"):
        self.con = sqlite3.connect(dbname)
        self.cursor = self.con.cursor()
        try:
            self.cursor.execute(Q_CREATE_TABLE)
        except sqlite3.OperationalError:
            pass # デーブルが既にある場合はパス

    def set_dict_factory(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        self.cursor.row_factory = dict_factory

    def set_row_factory(self):
        self.cursor.row_factory = None


    def add_website(self, id, img, url, title, description):
        self.cursor.execute(Q_INSERT, [id, img, url, title, description])
        self.con.commit()

    def get_website(self, id):
        self.set_dict_factory()
        for row in self.cursor.execute(Q_SELECT, [id]):
            self.set_row_factory()
            return row

    def get_image(self, id):
        for row in self.cursor.execute(Q_SELECT_IMG, [id]):
            return row[0]

    def __del__(self):
        self.con.close()
