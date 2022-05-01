import math
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON


endpoint = SPARQLWrapper("https://stko-kwg.geog.ucsb.edu/sparql")

prefixes = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX kwg-ont: <http://stko-kwg.geog.ucsb.edu/lod/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>"""

query = """
SELECT DISTINCT ?mudslide_id ?mudslide_description ?mudslide_date ?mudslide_geometry ?natural_disaster ?natural_disaster_description ?natural_disaster_start_date ?natural_disaster_end_date ?natural_disaster_geometry (group_concat(DISTINCT ?natural_disaster_date;separator=",") as ?natural_disaster_year)
WHERE {
    ?mudslide_id rdf:type kwg-ont:NOAADebrisFlow .
    ?mudslide_id kwg-ont:sfWithin ?mudslide_area .
    ?mudslide_id kwg-ont:hasTemporalScope ?mudslide_temporal_scope .
    ?mudslide_id kwg-ont:hasNarrative ?mudslide_description .
    ?mudslide_id geosparql:hasGeometry ?mudslide_geometry_node .
    ?mudslide_geometry_node geosparql:asWKT	?mudslide_geometry .

    ?mudslide_temporal_scope rdf:type time:Instant .
	?mudslide_temporal_scope time:inXSDDate ?mudslide_date .
    
    ?natural_disaster kwg-ont:sfWithin ?mudslide_area .
    ?natural_disaster rdf:type kwg-ont:Hazard .
	?natural_disaster kwg-ont:hasTemporalScope ?natural_disaster_temporal_scope .
    ?natural_disaster geosparql:hasGeometry ?natural_disaster_geometry_node .
    ?natural_disaster_geometry_node geosparql:asWKT	?natural_disaster_geometry .
    OPTIONAL {
        ?natural_disaster rdfs:label ?natural_disaster_description .
    }
    # Some fires only have time:Instant
    OPTIONAL {
        ?natural_disaster_temporal_scope rdf:type time:Instant .
        ?natural_disaster_temporal_scope time:inXSDgYear ?natural_disaster_date .
    }
    
    # Other fires have time:Interval dates
    OPTIONAL {
        ?natural_disaster_temporal_scope rdf:type time:Interval .
        ?natural_disaster_temporal_scope time:hasBeginning ?natural_disaster_start .
        ?natural_disaster_start time:inXSDDate ?natural_disaster_start_date .
        ?natural_disaster_temporal_scope time:hasEnd ?natural_disaster_end .
        ?natural_disaster_end time:inXSDDate ?natural_disaster_end_date .
    }

} GROUP BY ?mudslide_id ?mudslide_description ?mudslide_date ?mudslide_geometry ?natural_disaster ?natural_disaster_description ?natural_disaster_start_date ?natural_disaster_end_date ?natural_disaster_geometry"""

count_query = prefixes+'select (count(*) as ?count) {'+query+'}'
endpoint.setQuery(count_query)
endpoint.setReturnFormat(JSON)
results = endpoint.query().convert()
total_count = int(results['results']['bindings'][0]['count']['value'])

# If we query 10,000 results at a time, how many queries to we have to make?
num_queries = int(math.ceil(total_count/10000))
for query_index in range(num_queries):
    event_query = prefixes+query+f' OFFSET {10000*query_index} LIMIT 10000'
    endpoint.setQuery(event_query)
    endpoint.setReturnFormat(JSON)
    results = endpoint.query().convert()
    results = pd.io.json.json_normalize(results['results']['bindings'])
    results.to_csv(f'data/data-{query_index}.csv')
