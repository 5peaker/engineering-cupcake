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

@app.route("/no_content")
def no_content():
    return ({"message": "no content found"}, 204)

@app.route("/exp")
def make_response():
    res = make_response({"message": "hello, world"})
    res.status_code = 200
    return res

@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"{len(data)} records found"}
        else:
            return {"message": "no content found"}, 500
    except NameError:
        return {"message": "non existing data"}, 404

@app.route("/name_search")
def name_search():
    query = request.args.get("q")
    
    if not query:
        return {"message": "no query provided"}, 422
    
    for person in data:
        if query.lower() in person["name"].lower():
            return person
        
if __name__ == '__main__':
    app.run