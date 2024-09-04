# Import libraries
from flask import Flask, request, render_template, url_for, redirect

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {
        "id": 1,
        "data": "2024-01-05",
        "amount": 1000
    },
    {
        "id": 2,
        "data": "2024-03-05",
        "amount": 2000
    },
    {
        "id": 3,
        "data": "2024-06-05",
        "amount": 3000
    }
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route("/add", methods=["POST", "GET"])
def add_transaction():
    if request.method == "POST":
        new_transaction = {
            "id": len(transactions) + 1,
            "date": request.form["date"],
            "amount": float(request.form["amount"])
        }
        transactions.append(new_transaction)
        return redirect(url_for("get_transactions"))
    
    if request.method == "GET":
        return render_template("form.html")

# Update operation
@app.route("/edit/<int:transaction_id>", methods=["POST", "GET"])
def edit_transaction(transaction_id):
    if request.method == "GET":
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                return render_template("edit.html", transaction=transaction)
            
    if request.method == "POST":
        date = request.form["date"]
        amount = float(request.form["amount"])
        
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction["data"] = date
                transaction["amount"] = amount
                break 
            
            return redirect(url_for("get_transactions"))
        
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                return render_template("edit.html", transaction=transaction)

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transactions.remove(transaction)
            break
        
    return redirect(url_for("get_transactions"))

# add Search Transaction

# add Total Balance Function 

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)