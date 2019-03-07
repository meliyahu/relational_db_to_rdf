import rdflib
#from rdflib.plugins.sparql import prepareQuery
import os


def double_quote(word):
    '''
      Put quotes arround a string
    '''
    return '"%s"' % word


def findCvSampleUri(sampleId, cvType="SAMPLE_LEVEL"):
    '''
     Finds a tripl's uri (subject) whose hiddenLabel value is $sampleLevelId
    '''

    # Create an RDF graph based on the site-sample-level.ttl TTL file
    # The site-sample-level.ttl defines a common vacab for sample levels
    # which are foregn keys in the Site table, column value SAMPLELEVEL_ID
    g = rdflib.Graph()

    if (cvType == "SAMPLE_LEVEL"):
        cv_file = "site-sample-level.ttl"
    elif(cvType == "SAMPLE_TYPE"):
        cv_file = "site-sample-type.ttl"
    else:
       cv_file = "site-sample-level.ttl"

    g.parse(os.path.join("../model_ttl", cv_file), format='turtle')

    # print(f"Graph has {len(g)} statements")

    query = '''
    SELECT ?sampleURI WHERE {?search skos:hiddenLabel ''' + double_quote(sampleId) + '''. 
    bind(strafter(str(?search),"http://www.tern.org.au/cv/") as ?sampleURI)
    }'''

    qry_result = g.query(query)
    uri = ""
    if (len(qry_result) == 1):
        for row in qry_result:
            uri = row.sampleURI.toPython()
    else:
        print(
            f"No triples found for the pattern {'?s skos:hiddenLabel '} {double_quote(sampleId)}")

    if (uri):
        uri = uri.replace("/", ":")
        uri = "cv-" + uri

    return uri


if __name__ == "__main__":
    print("URI =", findCvSampleUri(3))
