import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required, timedelta
from flask_restful_swagger import swagger

from security.security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__, static_folder="static")
app.secret_key = "fabian"

# JWT Configurations
app.config["JWT_AUTH_URL_RULE"] = "/login" # Change endpint url
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800) # Change expration time
app.config["JWT_AUTH_USERNAME_KEY"] = "email" # Change username key
app.config["JWT_AUTH_HEADER_PREFIX"] = "Bearer" # Change prefix default JWT 
app.config["PROPAGATE_EXCEPTIONS"] = True

#SQL Alchemy Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#api = Api(app)

###################################
# Wrap the Api with swagger.docs.
api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/api/spec', description='REST API store')
###################################

#JWT
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
api.add_resource(User, "/user/<int:user_id>")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
