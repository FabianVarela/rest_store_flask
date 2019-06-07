from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    # Route methods HTTP
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {"message": "Store not found"}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "An store with name {} already exists".format(name)}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An exception occurred inserting the store"}, 500
        
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_item()

        return {"message": "store deleted"}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        result_stores = self.get_all()
        return {"stores": [store.json() for store in result_stores]}

    @classmethod
    def get_all(cls):
        return StoreModel.find_all()
