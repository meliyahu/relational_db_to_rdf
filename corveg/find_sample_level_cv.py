import rdflib
#from rdflib.plugins.sparql import prepareQuery
import os

def double_quote(word):
    '''
      Put quotes arround a string
    '''
    return '"%s"' % word


def findSampleLevelUri(sampleLevelId):
    '''
     Finds a tripl's uri (subject) whose hiddenLabel value is $sampleLevelId
    '''

    # Create an RDF graph based on the site-sample-level.ttl TTL file
    # The site-sample-level.ttl defines a common vacab for sample levels
    # which are foregn keys in the Site table, column value SAMPLELEVEL_ID
    g = rdflib.Graph()
    g.parse(os.path.join("../model_ttl", "site-sample-level.ttl"), format='turtle')
    # print(f"Graph has {len(g)} statements")

    query = '''
    SELECT ?sampleLevel WHERE {?search skos:hiddenLabel ''' + double_quote(sampleLevelId) + '''. 
    bind(strafter(str(?search),"http://www.tern.org.au/cv/") as ?sampleLevel)
    }'''

    qry_result = g.query(query)
    uri = ""
    if (len(qry_result) == 1):
        for row in qry_result:
            uri = row.sampleLevel.toPython()
    else:
        print(
            f"No triples found for the pattern {'?s skos:hiddenLabel '} {double_quote(sampleLevelId)}")

    if (uri):
        uri = uri.replace("/", ":")
        uri = "cv-" + uri

    return uri


if __name__ == "__main__":
    print("URI =", findSampleLevelUri(3))
