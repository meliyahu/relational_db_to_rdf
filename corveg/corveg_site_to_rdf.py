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
            print(f"Processing Corveg Site table. Site Id: {row['site_id']}.....")

            ttl_file.write(f"corveg:Site-{row['site_id']} \r\n")
            ttl_file.write(f"\trdf:type plot:Site ; \r\n")
            ttl_file.write(f'\tdct:description "{row["description"].strip()}" ; \r\n')
            ttl_file.write(f'\tdct:identifier "{row["site_number"].strip()}" ; \r\n')
            ttl_file.write(f'\tdct:modified "{row["entry_date"]}"^^xsd:date ; \r\n')
            ttl_file.write(f'\tdct:type {vocab.findCvSampleUri(row["samplelevel_id"],"SAMPLE_LEVEL")} ; \r\n')
            ttl_file.write(f'\tdct:type {vocab.findCvSampleUri(row["samplelevel_id"],"SAMPLE_TYPE")} ; \r\n')
            ttl_file.write(f"\tplot:siteDescription corveg:D-{row['site_id']} ; \r\n")
            ttl_file.write(f"\tlocn:location corveg:L-{row['location_id']} ; \r\n")
            ttl_file.write(f"\tprov:wasGeneratedBy corveg:P-{row['project_id']} ; \r\n")
            ttl_file.write(f'\tssn-ext:hasUltimateFeatureOfInterest bioregion:qld-CHC ; \r\n')
            ttl_file.write(". \r\n")

            # Description Observation Collection triples
            ttl_file.write(f"corveg:D-{row['site_id']} \r\n")
            ttl_file.write(f"\trdf:type ssn-ext:ObservationCollection ; \r\n")
            ttl_file.write(f"\trdf:type ogroup:Site-description ; \r\n")
            ttl_file.write(f'\trdfs:label "Site {row["site_id"]} basic description"@en ; \r\n')
            ttl_file.write(f'\tsosa:hasFeatureOfInterest corveg:Site-{row["site_id"]} ; \r\n')
            list_of_obs_dict = self.get_site_descrption_observations(row)
            for obs in list_of_obs_dict:
                ttl_file.write(f"\tssn-ext:hasMember corveg:{obs['uri']} ; \r\n")
                
            # ttl_file.write(f'\tsosa:phenomenonTime "{row["site_date"]}"^^xsd:dateTime ; \r\n')
            ttl_file.write(f'\tsosa:phenomenonTime corveg:T{row["site_date"]} ; \r\n')
            ttl_file.write(f'\tsosa:resultTime "{row["entry_date"]}"^^xsd:dataTime ; \r\n')
            ttl_file.write(". \r\n")
            # Process observations
            for obs in list_of_obs_dict:
                pass


        ttl_file.close()

        print(f"\nTTL generation completed.")
        print(f"\nProcessed {len(rows)} row/s of Corveg Site table.")
    
    def get_site_descrption_observations(self, row):
        '''
         Checks if description observations are captured.
         If so we want to create triples for the observations.
         If not, no triples need to be generated.
        '''
        observed_properties = []
        count = 0

        # Check Cover-litter observed property
        if (row['litter_percent'] is not None):
            count += 1
            uri = "D-" + str(row["site_id"]) + "-" + str(count)
            obs_prop = "Cover-litter"
            value = row['litter_percent']
            observed_properties.append({'uri': uri,'obs_prop': obs_prop, 'value': value})

        # Check Cover-rock observed property
        if (row['rock_percent'] is not None):
            count += 1
            uri = "D-" + str(row["site_id"]) + "-" + str(count)
            obs_prop = "Cover-rock"
            value = row['rock_percent']
            observed_properties.append({'uri': uri,'obs_prop': obs_prop, 'value': value})
        
        # Check Cover-bare observed property
        if (row['bare_percent'] is not None):
            count += 1
            uri = "D-" + str(row["site_id"]) + "-" + str(count)
            obs_prop = "Cover-bare"
            value = row['bare_percent']
            observed_properties.append({'uri': uri,'obs_prop': obs_prop, 'value': value})
        
        # Check Cover-crypto observed property
        if (row['crypto_percent'] is not None):
            count += 1
            uri = "D-" + str(row["site_id"]) + "-" + str(count)
            obs_prop = "Cover-crypto"
            value = row['crypto_percent']
            observed_properties.append({'uri': uri,'obs_prop': obs_prop, 'value': value})
        
        return observed_properties


if __name__ == "__main__":
    process = ProcessCorvegSiteTable()
    process.generateTTLFile(number_of_rows=2)
