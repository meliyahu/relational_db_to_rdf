import psycopg2 as pg
import psycopg2.extras as pg_ex
import os
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

    def write_uri_prifixes(self, file):
        file.write("@prefix ex-0: <http://www.tern.org.au/sites/> .\n")
        file.write("@prefix data: <http://www.tern.org.au/ns/data/> .\n")
        file.write("@prefix dct: <http://purl.org/dc/terms/> .\n")
        file.write("@prefix dwcterms: <http://rs.tdwg.org/dwc/terms/> .\n")
        file.write("@prefix geosparql: <http://www.opengis.net/ont/geosparql#> .\n")
        file.write("@prefix locn: <http://www.w3.org/ns/locn#> .\n")
        file.write("@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n")
        file.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
        file.write("@prefix plot: <http://www.tern.org.au/ns/plot/> .\n")
        file.write("@prefix plot-x: <http://www.tern.org.au/ns/plot/x/> .\n")
        file.write("@prefix prov: <http://www.w3.org/ns/prov#> .\n")
        file.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
        file.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
        file.write("@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n")
        file.write("@prefix sosa: <http://www.w3.org/ns/sosa/> .\n")
        file.write("@prefix ssn: <http://www.w3.org/ns/ssn/> .\n")
        file.write("@prefix ssn-ext: <http://www.w3.org/ns/ssn/ext/> .\n")
        file.write("@prefix time: <http://www.w3.org/2006/time#> .\n")
        file.write("@prefix w3cgeo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n")
        file.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
        file.write("@prefix cv-corveg: <http://www.tern.org.au/cv/corveg/> .\n")
        file.write("\n\r")


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
        self.write_uri_prifixes(ttl_file)

        for row in rows:
            print(f"ex-0:Site-{row['site_id']}")
            print(f"rdf:type plot:Site ;")
            print(f'dct:description "{row["description"].strip()}" ;')
            print(f'dct:identifier "{row["site_number"].strip()}" ;')
            print(f'dct:modified "{row["site_date"]}"^^xsd:date ;')
            print(f'dct:type {sl_vocab.findSampleLevelUri(row["samplelevel_id"])} ;')
            print(".")
            print("")

            ##
            ttl_file.write(f"ex-0:Site-{row['site_id']} \r\n")
            ttl_file.write(f"\trdf:type plot:Site ; \r\n")
            ttl_file.write(f'\tdct:description "{row["description"].strip()}" ; \r\n')
            ttl_file.write(f'\tdct:identifier "{row["site_number"].strip()}" ; \r\n')
            ttl_file.write(f'\tdct:modified "{row["site_date"]}"^^xsd:date ; \r\n')
            ttl_file.write(f'\tdct:type {sl_vocab.findSampleLevelUri(row["samplelevel_id"])} ; \r\n')
            ttl_file.write(". \r\n")
            # ttl_file.write("")

        ttl_file.close()


if __name__ == "__main__":
    process = ProcessCorvegSiteTable()
    process.generateTTLFile()
