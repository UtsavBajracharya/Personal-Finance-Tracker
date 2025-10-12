from flask import Flask, render_template, request, url_for, make_response, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = 'my-secret-key'
db = SQLAlchemy(app)

# create database model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)


with app.app_context():
    db.create_all()
    
CATEGORIES = ['Food', 'Transport', 'Rent', 'Utilities', 'Health']



@app.route("/")
def index():

    expenses = Expense.query.order_by(Expense.date.desc(), Expense.id.desc()).all()
    total = round(sum(e.amount for e in expenses))

    return render_template(

        "index.html", 

        expenses=expenses,
        categories=CATEGORIES,
        total=total
        
    )

# add route for expense form
@app.route("/add", methods=['POST'])
def add():

    description = (request.form.get("description") or "").strip() #returns a string instead of none and prevent that error from happening
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    # Form handling
    if not description or not amount_str or not category:
        flash("Please fill description, amount, and category", "error")
        return redirect(url_for("index"))

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError

    except ValueError:
        flash("Amount must be a positive number", "error")
        return redirect(url_for("index"))


    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()

    except ValueError:
        d = date.today    

    e = Expense(description=description, amount=amount, category=category, date=d)
    db.session.add(e)
    db.session.commit()

    flash("Expense added", "success")
    return redirect(url_for("index"))


    print("Form Received:", dict(request.form))
    return make_response("Form received check the console")

# Detete expenses
@app.route("/delete/<int:expense_id>", methods=['POST'])
def delete(expense_id):
    e = Expense.query.get_or_404(expense_id)
    db.session.delete(e)
    db.session.commit()
    flash("Expense deleted", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

