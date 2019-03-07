import psycopg2 as pg
import psycopg2.extras as pg_ex
import sys
sys.path.append("..")
import config as cfg
import rdflib
import find_sample_level_cv as sl_vocab

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
            print(f"ex-0:Site-{row['site_id']}")
            print(f"rdf:type plot:Site ;")
            print(f'dct:description "{row["description"].strip()}" ;')
            print(f'dct:identifier "{row["site_number"].strip()}" ;')
            print(f'dct:modified "{row["site_date"]}"^^xsd:date ;')
            print(f'dct:type {sl_vocab.findSampleLevelUri(row["samplelevel_id"])} ;')
            print(".")
            print("")


if __name__ == "__main__":
    process = ProcessCorvegSiteTable()
    process.generateTTLFile()
