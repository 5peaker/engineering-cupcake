from flask import Flask, request
app = Flask(__name__) 

data = [
    {
        "name": "John",
        "age": 30,
        "city": "New York"
    },
    {
        "name": "Jane",
        "age": 25,
        "city": "Los Angeles"
    },
    {
        "name": "Joe",
        "age": 20,
        "city": "Chicago"
    }
] 

@app.route('/')
def index():
    return "hello, world!"

@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"{len(data)} records found"}
        else:
            return {"message": "no content found"}, 500
    except NameError:
        return {"message": "non existing data"}, 404
    
@app.route("/count")
def count():
    try:
        return {"data count": len(data)}, 200
    except NameError:
        return {"message": "non existing data"}, 500
    
@app.route("/person/<var_name>")
def find_by_uuid_age(var_name):
    for person in data:
        if person["name"] == str(var_name):
            return person
        else:
            return{"message": "no people found"}, 404

@app.route("/person/<var_name>", methods=["DELETE"])
def delete_by_name(var_name):
    for person in data:
        if person["name"] == str(var_name):
            data.remove(person)
            return {"message": f"deleted person with the name {var_name}, yeah!"}, 200
        else:
            return {"message": "no people found"}, 404
        
@app.route("/person", methods=["POST"])
def new_person():
    new_person = request.get_json()
    if not new_person:
        return {"message", "invaild input"}, 400
    else:
        return {"message": "welcome new person!"}, 201

@app.errorhandler(404)
def api_not_found(error):
    return {"message": "some error"}, 404

if __name__ == '__main__':
    app.run