import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required, timedelta
from flask_jwt_extended import JWTManager
from flask_restful_swagger import swagger

from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__, static_folder="static")
app.secret_key = "fabian"

# JWT Configurations
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=1800) # Change expration time
app.config["JWT_HEADER_TYPE"] = "Bearer" # Change prefix, default JWT 

#SQL Alchemy Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#api = Api(app)

###################################
# Wrap the Api with swagger.docs.
api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/api/spec', description='REST API store')
###################################

#JWT
jwt = JWTManager(app)

# Add resources or routes
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
