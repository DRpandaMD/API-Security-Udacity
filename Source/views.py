# views.py
# handles application routing

from models import Base, User
from flask import Flask, jsonify, request, url_for, abort, json, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user    # a reference to a global?
    return True


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.args['username']
    password = request.args['password']
    print(request)
    # we need to check for missing information and abort out
    if username is None or password is None:
        print("there is no username or password")
        abort(400)
    if session.query(User).filter_by(username=username).first() is not None:
        print("existing user")
        abort(400)  # here the user already exists
    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}


@app.route('/api/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
        return jsonify({'username': user.username})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello: ' + g.user.username})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)