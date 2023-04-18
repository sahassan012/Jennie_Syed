from pymongo import MongoClient
# You don't need to change any of it
# Making Connection
myclient = MongoClient("mongodb://localhost:27017/")

# database
db = myclient["academicworld"]
collection = db["faculty"]

def find_professor():
    user_input_name = input("Enter the name: ")
    # Li,Qun
    user_input_name = str(user_input_name)
    professor_name = {"name" : "{}".format(user_input_name)}
    professor_column = {"name":1, "position":1, "researchInterest":1, "email":1, "phone":1, "photoUrl":1, "affiliation.name":1, "_id":0}

    faculty_data= collection.find(professor_name, professor_column)
    data_set = {}
    for data in faculty_data:
        data_set["name"] = data["name"]
        data_set["photoUrl"] = data["photoUrl"]
        data_set["email"] = data["email"]
        data_set["phone"] = data["phone"]
        data_set["researchInterest"] = data["researchInterest"]
        data_set["position"] = data["position"]
        affiliation = data["affiliation"]
        data_set["affiliation"] = affiliation["name"]

    print(data_set)

    return data_set
