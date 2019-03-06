import psycopg2 as pg
import sys
sys.path.append("..")
import config as cfg


class ProcessCorvegSiteTable:
    def __init__(self):
        params = cfg.config('corveg_database.ini')
        self.conn = pg.connect(**params)
        self.cur = self.conn.cursor()

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
        print(rows)


if __name__ == "__main__":
    process = ProcessCorvegSiteTable()
    process.generateTTLFile()
