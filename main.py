from flask import Flask,render_template, session
from flask import request
from model import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.secret_key = 'your_secret_key_here'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    user = User.query.get(session.get('user_id')) if session.get('user_id') else None
    return render_template("home.html", user=user)

@app.route("/about")
def about():
    user = User.query.get(session.get('user_id')) if session.get('user_id') else None
    return render_template("about.html", user=user)

@app.route("/signup",methods=["POST","GET"])
def signup():
    user = User.query.get(session.get('user_id')) if session.get('user_id') else None
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        db_user=User.query.filter_by(email=email).first()
        if db_user:
            return render_template("Signup.html",error="Email already exists", user=user)
        db_user=User.query.filter_by(name=name).first()
        if db_user:
            return render_template("Signup.html",error="Name already exists", user=user)
        user=User(name=name,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return render_template("Login.html", user=user)    
    return render_template("Signup.html", user=user)

        

@app.route("/login",methods=["POST","GET"])
def login():
    user = User.query.get(session.get('user_id')) if session.get('user_id') else None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        db_user=User.query.filter_by(email=email,password=password).first()
        if db_user:
            session["user_id"]=db_user.id
            return render_template("home.html",user=db_user)
        else:
            return render_template("login.html", user=user)
    return render_template("login.html", user=user)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return render_template("home.html",user=None)


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)