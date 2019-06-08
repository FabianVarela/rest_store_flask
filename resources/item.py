from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.item import ItemModel

class Item(Resource):
    # Parser data
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field is required"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )
    
    # Route methods HTTP
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return {"message": "Item not found"}, 404

    @jwt_required
    #@fresh_jwt_required #Only use a fresh token fresh=True
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An exception occurred inserting the item"}, 500
        
        return item.json(), 201

    @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()

        if not claims["is_admin"]:
            return {"message", "Admin privilege required"}, 401

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_item()

        return {"message": "item deleted"}


class ItemList(Resource):
    # Route methods HTTP
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        result_items = [item.json() for item in self.get_all()]

        if user_id:
            return {"items": result_items}, 200

        return {
            "items": [item["name"] for item in result_items],
            "message": "More data available if you log in"
        }, 200

    # Class methods
    @classmethod
    def get_all(cls):
        return ItemModel.find_all()
