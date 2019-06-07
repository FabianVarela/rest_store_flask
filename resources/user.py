from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_restful_swagger import swagger
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token

# Parser data
_user_parser = reqparse.RequestParser()

_user_parser.add_argument("username", type=str, required=True, help="This field cannot be in blank")
_user_parser.add_argument("password", type=str, required=True, help="This field cannot be in blank")

class UserRegister(Resource):
    # Route methods HTTP

    "Register user"
    @swagger.operation(
        notes="Register a new user",
        responseClass=UserModel.__name__,
        nickname="register",
        parameters=[
            {
                "name": "user body",
	            "description": "User's username and password",
                "required": True,
                "allowMultiple": False,
                "dataType": UserModel.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
              "code": 201,
              "message": "Username created"
            },
            {
              "code": 400,
              "message": "Invalid input or user already exists"
            },
            {
              "code": 500,
              "message": "Internal server error"
            }
        ]
    )
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.insert()

        return {"message": "User created successfully"}, 201

class User(Resource):
  @classmethod
  def get(cls, user_id):
    user = UserModel.find_by_id(user_id)
    
    if not user:
      return {"message": "User not found"}, 404

    return user.json()
  
  @classmethod
  def delete(cls, user_id):
    user = UserModel.find_by_id(user_id)

    if not user:
      return {"message": "User not found"}, 404

    user.delete_from_db()
    return {"message": "User deleted"}, 200

class UserLogin(Resource):
  def post(self):
    data = _user_parser.parse_args()

    user = UserModel.find_by_username(data["username"])

    if user and safe_str_cmp(user.password, data["password"]):
      access_token = create_access_token(identity=user.id, fresh=True)
      refresh_token = create_refresh_token(user.id)
      
      return {
        "access_token": access_token,
        "refresh_token": refresh_token
      }, 200

    return {"message": "Invalid credentials"}, 401
