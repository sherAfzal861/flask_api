# from datetime import datetime
# from flask import abort, make_response
# def get_timestamp():
#     return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# PEOPLE = {
#     "Fairy":{
#        "fname": "Tooth",
#        "lname": "FAiry",
#        "timestamp": get_timestamp(), 
#     },
#     "Ruprecht": {
#         "fname": "Knecht",
#         "lname": "Fairy",
#         "timestamp": get_timestamp(),
#     },
#     "Bunny":{
#         "fname": "Easter",
#         "lname": "Bunny",
#         "timestamp": get_timestamp(),
#     },
# }

# def read_all():
#     return list(PEOPLE.values())

# def create(person):
#     lname = person.get("lname")
#     fname = person.get("fname", "")
    
#     if lname and lname not in PEOPLE:
#         PEOPLE[lname] = {
#             "lname": lname,
#             "fname": fname,
#             "timestamp": get_timestamp(),
#         }
#         return PEOPLE[lname], 201
    
#     else:
#         abort(
#             406,
#             f"Person with last name {lname} already exists"
#         )

# def read_one(lname):
#     if lname in PEOPLE:
#         return PEOPLE[lname]
#     else:
#         abort(
#             404, f"person with last name {lname} not found"
#         )
        
        
# def update(lname, person):
#     if lname in PEOPLE:
#         PEOPLE[lname]["fname"] = person.get("fname", PEOPLE[lname]["fname"])
#         PEOPLE[lname]["timestamp"] = get_timestamp()
#         return PEOPLE[lname]
#     else:
#         abort(
#             404,
#             f"Person with last name {lname} not found"
#         )
        
# def delete(lname):
#     if lname in PEOPLE:
#         del PEOPLE[lname]
#         return make_response(
#             f"{lname} successfully deleted", 200
#         )
#     else:
#         abort(
#             404,
#             f"person with last name {lname} not found"
#         )


#WITH DATABASE
from flask import make_response, abort
from config import db
from models import Person, PersonSchema, person_schema, people_schema
# people_schema=PersonSchema(many=True)
def read_all():
    people = Person.query.all()
    return people_schema.dump(people)

def read_one(lname):
    person = Person.query.filter(Person.lname==lname).one_or_none()
    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with last name {lname} not found")
def create(person):
    lname = person.get("lname")
    existing_peson = Person.query.filter(Person.lname == lname).one_or_none()
    
    if existing_peson is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Person with last name {lname} already exists")
def delete(lname):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404, f"Person with last name {lname} not found")
def update(lname, person):
    existing_person = Person.query.filter(Person.lname==lname).one_or_none()
    
    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with last name {lname} not found")