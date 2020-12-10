from datetime import timedelta

from flask import Flask, request, make_response, session, jsonify
import json

from flask_sqlalchemy import SQLAlchemy
from requests.auth import HTTPBasicAuth

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/registration'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
app.secret_key = "secret key"
db=SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column('id',db.Integer(),primary_key=True)
    name = db.Column('name',db.String(100))
    password = db.Column('password',db.String(100))
    email = db.Column('email',db.String(100))
    phonenumber= db.Column('phonenumber',db.Integer())
    active = db.Column('active',db.String(100),default='Y')

# db.create_all()

@app.route("/customer/",methods=["GET"])
def welcome_user_page():
    if 'name' in session:
        username = session['name']
        return jsonify({'message': 'You are already logged in', 'username': username})
    else:
        resp = jsonify({'message': 'You have to login...'})
        resp.status_code = 401
        return resp
    # return "User REST API Endpoints are working..!"

@app.route("/customer/",methods=["POST"])
def save_data():
    reqdata= request.get_json()

    email=reqdata["email"]
    if Customer.query.filter(Customer.email == email).first():
        return {"status":"duplicate email address...{}!".format(email)}

    #print(reqdata)
    custmodel =Customer(name=reqdata["name"],password=reqdata["password"],email=reqdata["email"],phonenumber=reqdata["phonenumber"])
    db.session.add(custmodel)
    db.session.commit()
    return {"success": "Customer <{}> saved successfully" .format(custmodel.id)}

@app.route("/login/",methods=["POST"])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message' : 'Bad Request - invalid credendtials'})

    user = Customer.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Username or Password wrong', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


    if user.password == auth.password:
        session['name'] = auth.username
        return jsonify({'message' : 'You are logged in successfully'})

    return make_response('Either name or password wrong', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/logout/')
def logout():
    if 'name' in session:
        session.pop('name', None)
    return jsonify({'message': 'You successfully logged out'})



if __name__=='__main__':
    app.run(debug=True)
    
    
    
    
 #New line added
 ##added something new