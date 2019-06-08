import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_restful_swagger import swagger
from datetime import timedelta

from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__, static_folder="static")
app.secret_key = "fabian"

# JWT Configurations
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=1800) # Change expration time
app.config["JWT_HEADER_TYPE"] = "Bearer" # Change prefix, default JWT 
app.config['PROPAGATE_EXCEPTIONS'] = True # Propagate exception

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

# Method to manage claims and permissions
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Can be replaced by other configuration
        return {"is_admin": True}
    
    return {"is_admin": False}

# Message when the token has expired
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": "The token has been expired",
        "error": "token_expired"
    }), 401

# Message when the token is invalid
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": "Signature verification failed",
        "error": "invalid_token"
    }), 401

# Message when the request does not send the token
@jwt.unathorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request doesn't containt an access token",
        "error": "authorization_required"
    }), 401

# Message when the token is not fresh
@jwt.needs_fresh_token_loader
def token_not_refresh_callback():
    return jsonify({
        "description": "The token is not fresh",
        "error": "fresh_token_required"
    }), 401

# Message when the token has expired and has been revoked
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked",
        "error": "token_revoked"
    }), 401

# Add resources or routes
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
