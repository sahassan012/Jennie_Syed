from MongoDB_utils import find_professor
from Mysql_utils import  create_my_table, update_my_table, delete_my_table, create_top10_professors_by_school, create_top10_professors_by_keywords
from Neo4j__utils import create_top10_professors_by_publications

# faculty page
# Using MongoDB
find_professor()

# Using Mysql
# Make our personal tables for manage my professors
# We can update and delete
create_my_table("MyProfessor")
update_my_table()
delete_my_table()
create_top10_professors_by_publications()
create_top10_professors_by_keywords()
#Neo4J
create_top10_professors_by_publications()
