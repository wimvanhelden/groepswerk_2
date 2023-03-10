from flask import Flask, render_template, url_for, flash, redirect
from .forms import RegistrationForm, LoginForm
from . import app

#dummy data for books (development): 
books_dict = [   
    {'author':'Umberto Eco',
     'title': "De naam van de roos",
    'description' : "Brilliante detectivethriller uit de middeleeuwen"},
    {'author': "Gabrial Garcia Marquez",
     "title": "Honderd jaar eenzaamheid",
     'description': "Magisch realisme in een fictief zuid amerikaans land"},
    {'author': 'Hendrik Consience',
     'title':'De leeuw van Vlaanderen',
     'description': 'Klassieker over de guldensporenslag'} 
]



@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/books")
def books():
    return render_template("books.html", title="books",  books=books_dict)  #books.html handles books_dict == None or books_dict empty


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created! You are now able to log in!', 'success')
        return redirect(url_for('login'))   #we can change this: automaticaly login and redirect to home? 
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # finish later... 
        flash('Login Succesfull!')
        pass
    else:
        flash('Login unsuccesful... Please check login/password!')
    return render_template("login.html", title = "Login", form=form)
