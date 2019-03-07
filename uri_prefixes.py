
def write_uri_prifixes(file):
    '''
      Prepends the uri prefixes to a passed in file
    '''
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
