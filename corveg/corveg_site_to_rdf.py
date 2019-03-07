import rdflib
import psycopg2 as pg
import psycopg2.extras as pg_ex
import os
import sys
sys.path.append("..")
import find_sample_cv as vocab
import config as cfg
from uri_prefixes import write_uri_prifixes


class ProcessCorvegSiteTable:
    def __init__(self):
        params = cfg.config(filename='corveg_database.ini')
        self.conn = pg.connect(**params)
        self.cur = self.conn.cursor(cursor_factory=pg_ex.DictCursor)

    def generateTTLFile(self, number_of_rows=10):
        try:
            self.cur.execute('SELECT * FROM site LIMIT ' + str(number_of_rows))
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
            ttl_file.write(f"ex-0:Site-{row['site_id']} \r\n")
            ttl_file.write(f"\trdf:type plot:Site ; \r\n")
            ttl_file.write(f'\tdct:description "{row["description"].strip()}" ; \r\n')
            ttl_file.write(f'\tdct:identifier "{row["site_number"].strip()}" ; \r\n')
            ttl_file.write(f'\tdct:modified "{row["site_date"]}"^^xsd:date ; \r\n')
            ttl_file.write(f'\tdct:type {vocab.findCvSampleUri(row["samplelevel_id"],"SAMPLE_LEVEL")} ; \r\n')
            ttl_file.write(f'\tdct:type {vocab.findCvSampleUri(row["samplelevel_id"],"SAMPLE_TYPE")} ; \r\n')
            ttl_file.write(f"\tplot:siteDescription ex-0:D-{row['site_id']}-1 ; \r\n")
            ttl_file.write(f"\tlocn:location ex-0:L-{row['location_id']} ; \r\n")
            ttl_file.write(f"\tprov:wasGeneratedBy ex-0:P-{row['project_id']} ; \r\n")

            ttl_file.write(f'\tssn-ext:hasUltimateFeatureOfInterest bioregion:qld-CHC ; \r\n')
            ttl_file.write(". \r\n")
            # ttl_file.write("")

        ttl_file.close()


if __name__ == "__main__":
    process = ProcessCorvegSiteTable()
    process.generateTTLFile(number_of_rows=2)
