import mysql.connector
from MongoDB_utils import find_professor

mydb = mysql.connector.connect(
    host="localhost",
    user="root", # You need your username for mysql
    password="test_root", # You need your password for mysql
    database="academicworld"
)

mycursor = mydb.cursor()

def create_my_table(MyProfessor):
    query = "DROP TABLE IF EXISTS {}".format(MyProfessor)
    drop_table = mycursor.execute(query)

    query = """
        CREATE TABLE {} (
          id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(255) NOT NULL,
          phone VARCHAR(20) NOT NULL,
          email VARCHAR(255) NOT NULL,
          university VARCHAR(255) NOT NULL
        )
        """.format(MyProfessor)
    create_table = mycursor.execute(query)

    query = "SHOW INDEX FROM {} WHERE Key_name = 'myindex'".format(MyProfessor)
    mycursor.execute(query)
    # check if the index exists
    index_exists = mycursor.fetchone() is not None
    if index_exists:
        mycursor.execute("DROP INDEX myindex ON {}".format(MyProfessor))
        mydb.commit()
    else:
        mycursor.execute("CREATE INDEX myindex ON {} (name)".format(MyProfessor))

    return print("MyProfessor table is created")

def update_my_table(professor):
    data = find_professor(professor)
    table_name = 'MyProfessor'
    name = data["name"]
    phone = data["phone"]
    email = data["email"]
    university = data["affiliation"]
    insert_query = "INSERT INTO " + table_name + " (name, phone, email, university) VALUES ('{}', '{}', '{}', '{}')".format(name, phone, email, university)
    update_table = mycursor.execute(insert_query)
    mydb.commit()
    mycursor.execute("select * from MyProfessor")
    result = mycursor.fetchall()
    print(result)
    return result

def delete_my_table(professor):
    #user_input_name = input("Enter the name: ")
    user_input_name = professor
    delete_query = "Delete from MyProfessor where name = \"{}\"".format(user_input_name)
    delete_professor = mycursor.execute(delete_query)
    mydb.commit()
    mycursor.execute("select * from MyProfessor")
    result = mycursor.fetchall()
    print(result)
    return result

# Find the top-10 faculty members who have the most publications for the user input school
def create_top10_professors_by_school():
    user_input_name = input("Enter the school name: ")
    user_input_name = str(user_input_name)
    university_id = "select id from university where name = \"{}\"".format(user_input_name)
    mycursor.execute(university_id)
    result = mycursor.fetchall()
    university_id = result[0][0]

    check_view_sql = """
        SELECT COUNT(*)
        FROM information_schema.views
        WHERE table_schema = 'academicworld'
        AND table_name = 'top10_professors_by_publications';
        """
    mycursor.execute(check_view_sql)
    result = mycursor.fetchone()
    # If the result is 1, drop the view
    if result[0] == 1:
        drop_view_sql = "DROP VIEW top10_professors_by_publications;"
        mycursor.execute(drop_view_sql)
        print("View dropped")

    # Define the SQL command to create the view
    create_view_sql = """
    CREATE VIEW top10_professors_by_publications AS
    SELECT name, count(title) from faculty_publication, publication, faculty
    where publication.id = faculty_publication.publication_id and
    faculty_id = faculty.id and university_id = {}
    group by name order by count(title) desc limit 10;
    """.format(university_id)

    # Execute the SQL command to create the view
    mycursor.execute(create_view_sql)

    # Commit the changes to the database
    mydb.commit()

    mycursor.execute("select * from top10_professors_by_publications")
    result = mycursor.fetchall()
    print(result)
    mydb.close()
    return result

# Find the top-10 faculty members who have the highest keyword-relevant citations for the user input keyword
def create_top10_professors_by_keywords():
    user_input_keywords = input("Enter the keywords: ")
    user_input_keywords = str(user_input_keywords)

    check_view_sql = """
        SELECT COUNT(*)
        FROM information_schema.views
        WHERE table_schema = 'academicworld'
        AND table_name = 'top10_professors_by_keywords';
        """
    mycursor.execute(check_view_sql)
    result = mycursor.fetchone()
    # If the result is 1, drop the view
    if result[0] == 1:
        drop_view_sql = "DROP VIEW top10_professors_by_keywords;"
        mycursor.execute(drop_view_sql)
        print("View dropped")

    create_view_sql = """
    CREATE VIEW top10_professors_by_keywords AS
    select name, sum(TMP.KRC) as KRC from faculty,
    (select faculty_id, faculty_publication.publication_id, KRC from faculty_publication,
    (select publication_id, score*num_citations as KRC from publication_keyword, publication
    where publication_id = publication.id and keyword_id = (select id from keyword where name = \"{}\")) as KW
    where faculty_publication.publication_id = KW.publication_id) as TMP
    where faculty.id = TMP.faculty_id
    group by name
    order by KRC desc limit 10;
    """.format(user_input_keywords)

    mycursor.execute(create_view_sql)

    # Commit the changes to the database
    mydb.commit()

    mycursor.execute("select * from top10_professors_by_keywords")
    result = mycursor.fetchall()
    print(result)
    #mydb.close()
    return result




















#mycursor.execute("show tables")
#myresult = mycursor.fetchall()
#print(myresult)
