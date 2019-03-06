import psycopg2 as pg
import psycopg2.extras as pg_ex
import sys
sys.path.append("..")
import config as cfg


class ProcessCorvegSiteTable:
    def __init__(self):
        params = cfg.config(filename='corveg_database.ini')
        self.conn = pg.connect(**params)
        self.cur = self.conn.cursor(cursor_factory=pg_ex.DictCursor)

    def generateTTLFile(self):
        try:
            self.cur.execute('SELECT * FROM site LIMIT 10')
            rows = self.cur.fetchall()
            self.__process(rows)
        except (Exception, pg.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def __process(self, rows):
        # TODO implement later
        for row in rows:
            print(f"Site Id: {row['site_id']}")
            print(f"Description: {row['description']}\n")


if __name__ == "__main__":
    process = ProcessCorvegSiteTable()
    process.generateTTLFile()
