# views.py
# handles the work load for the app

from models import Base, User, Bagel
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite://bagelShop.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession

app = Flask(__name__)


# add @auth.verify here:
@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user    # a reference to a global?
    return True


# add the /users route here
@app.route('/users', methods=['POST'])
def new_user():
    username = request.args['username']
    password = request.get_json['password']
    # we need to check for missing information and abort out
    if username is None or password is None:
        abort(400)
    if session.query(User).filter_by(username=username).first() is not None:
        print("existing user")
        abort(400)  # here the user already exists
    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}


@app.route('/bagels', methods=['GET', 'POST'])
@auth.login_required
def show_all_bagels():
    if request.method == 'GET':
        bagels = session.querey(Bagel).all()
        return jsonify(bagels=[bagel.serialize for bagel in bagels])
    elif request.method == 'POST':
        name = request.args['name']
        description = request.args['description']
        picture = request.agrs['picture']
        price = request.args['price']
        newBagel = Bagel(name=name, description=description, picture=picture, price=price)
        session.add(newBagel)
        session.commit()
        return jsonify(newBagel.serialize)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
