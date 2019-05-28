from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_restful_swagger import swagger

class UserRegister(Resource):
    # Parser data
    parser = reqparse.RequestParser()

    parser.add_argument("username", type=str, required=True, help="This field cannot be in blank")
    parser.add_argument("password", type=str, required=True, help="This field cannot be in blank")

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
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data["username"], data["password"])
        user.insert()

        return {"message": "User created successfully"}, 201
