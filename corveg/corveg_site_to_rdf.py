import psycopg2 as pg
import psycopg2.extras as pg_ex
import os
import sys
sys.path.append("..")
import config as cfg
import rdflib
import find_sample_cv as sl_vocab
from uri_prefixes import write_uri_prifixes

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

        ttl_file = open(os.path.join("../ttl_output", "corveg-site.ttl"), "w+") 
        write_uri_prifixes(ttl_file)

        for row in rows:
            # print(f"ex-0:Site-{row['site_id']}")
            # print(f"rdf:type plot:Site ;")
            # print(f'dct:description "{row["description"].strip()}" ;')
            # print(f'dct:identifier "{row["site_number"].strip()}" ;')
            # print(f'dct:modified "{row["site_date"]}"^^xsd:date ;')
            # print(f'dct:type {sl_vocab.findCvSampleUri(row["samplelevel_id"], "SAMPLE_LEVEL")} ;')
            # print(f'dct:type {sl_vocab.findCvSampleUri(row["sampletype_id"],"SAMPLE_TYPE")} ;')
            # print(".")
            # print("")

            ##
            ttl_file.write(f"ex-0:Site-{row['site_id']} \r\n")
            ttl_file.write(f"\trdf:type plot:Site ; \r\n")
            ttl_file.write(f'\tdct:description "{row["description"].strip()}" ; \r\n')
            ttl_file.write(f'\tdct:identifier "{row["site_number"].strip()}" ; \r\n')
            ttl_file.write(f'\tdct:modified "{row["site_date"]}"^^xsd:date ; \r\n')
            ttl_file.write(f'\tdct:type {sl_vocab.findCvSampleUri(row["samplelevel_id"],"SAMPLE_LEVEL")} ; \r\n')
            ttl_file.write(f'\tdct:type {sl_vocab.findCvSampleUri(row["samplelevel_id"],"SAMPLE_TYPE")} ; \r\n')
            ttl_file.write(". \r\n")
            # ttl_file.write("")

        ttl_file.close()


if __name__ == "__main__":
    process = ProcessCorvegSiteTable()
    process.generateTTLFile()
