from flask import Flask ,redirect,url_for, render_template, request, session, flash
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy.sql.expression import select
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from twilio.twiml.messaging_response import MessagingResponse
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import current_user
from flask_login import login_user, login_required, logout_user 
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path


app = Flask(__name__)

# create db for expenditures    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exp.db'
dbt = SQLAlchemy(app)

# db model 
class Exp(dbt.Model):
    id = dbt.Column(dbt.Integer, primary_key=True)
    title = dbt.Column(dbt.String(100), nullable=False)
    price = dbt.Column(dbt.Integer(), nullable=False)
    date_created = dbt.Column(dbt.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
            return f"Post('{self.title}', '{self.content}')"
dbt.create_all(app=app)

# page routes 
@app.route("/", methods=["GET", "POST"])
def index():
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
        return render_template("login.html")

@app.route("/about", methods=["GET", "POST"])
def about():
        return render_template("about.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard(): 
        return render_template("dashboard.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
        return render_template("contact.html")



@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply

    exp_list = list()
    exp_price = dbt.session.query(Exp.price).all()
    exp_title = dbt.session.query(Exp.title).all()

    exp_list= (exp_title)

    budget = 0 
    total = 0 


    resp = MessagingResponse()
    if 'spent: '.lower() in msg:
        exp_title = msg.split(':')[1]
        exp_price = msg.split(',')[1]

        new_exp = Exp(title=exp_title, price=exp_price )
        dbt.session.add(new_exp)
        dbt.session.commit()

        # for j in exp_price:
        #     for n in j: 
        #         n = int(n)
        #         total = total + n 

        
        resp.message(f"Successfully added a new expenditure")

    elif '-show exp'.lower() in msg:

        for i in exp_list:
            resp.message(f"exp {i}")

    elif 'budget: '.lower() in msg: 
        budget = msg.split(':')[1]

        resp.message(f"Your montly budget set as: {budget}")

    elif '-view'.lower() in msg: 
        for j in exp_price:
            for n in j: 
                n = int(n)
                total = total + n 

        resp.message(f'Budget: {200} \n Total expediture: {total}')

    elif '-help'.lower() in msg: 
        resp.message(f'Commands: \n \n spent: [title], [price] = To add a new expenditure \n -show exp = To show all the expenditures \n budget: [budget] = To set a monthly budget \n -view = To view your montly budget and total expenditure')
        
    else:
        resp.message(f"Hii, Use /help to a list of all commands ")



    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)