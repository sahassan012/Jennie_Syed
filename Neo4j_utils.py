from neo4j import GraphDatabase


uri = "bolt://localhost:7687"
user = "neo4j"  # You need to make your own user name and password for connection
password = "Nspider0603"

driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False, database="academicworld")

#TOP 10 professors and school with the most publication
def create_top10_professors_by_publications():
    query = """ MATCH(institute:INSTITUTE) -[r:AFFILIATION_WITH]-(faculty:FACULTY)-[:PUBLISH]-(publication:PUBLICATION)
    WITH institute, faculty, COUNT(publication) AS num_publications
    ORDER BY num_publications DESC
    RETURN faculty.name, institute.name, num_publications
    LIMIT 10 """

    data = []
    with driver.session() as session:
        results = session.run(query)
        for record in results:
            #print(record)
            data.append(record)

    print(data)

    return data

driver.close()
