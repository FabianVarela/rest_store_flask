from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required, timedelta

from security.security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.secret_key = "fabian"

# JWT Configurations
app.config["JWT_AUTH_URL_RULE"] = "/login" # Change endpint url
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800) # Change expration time
app.config["JWT_AUTH_USERNAME_KEY"] = "email" # Change username key
app.config["JWT_AUTH_HEADER_PREFIX"] = "Bearer" # Change prefix default JWT 

#SQL Alchemy Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)
jwt = JWT(app, authenticate, identity)

@jwt.auth_response_handler
def custom_response_jwt(access_token, identity):
    return jsonify({
        "access_token": access_token.decode("utf-8"),
        "user_id": identity.id
    })

@jwt.jwt_error_handler
def custom_error_response_jwt(error):
    return jsonify({
        "message": error.description,
        "code": error.status_code
    }), error.status_code

# Add resources or routes
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

db.init_app(app)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
