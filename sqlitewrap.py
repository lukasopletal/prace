import sqlite3


class SQLite:
    def __init__(self, file="data.sqlite3"):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


########################################################################################

if __name__ == "__main__":
    with SQLite("data.db") as cur:
        res = cur.execute("SELECT * FROM table where a=?", [2])
        for x in res.fetchall():
            print(x)
