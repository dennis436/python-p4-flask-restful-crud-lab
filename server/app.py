#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


# GET and POST /plants
class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plants_list = [plant.to_dict() for plant in plants]
        return make_response(jsonify(plants_list), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


# GET, PATCH, DELETE /plants/<int:id>
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            return make_response(plant.to_dict(), 200)
        return make_response({"error": "Plant not found"}, 404)

    def patch(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return make_response({"error": "Plant not found"}, 404)

        data = request.get_json()
        for attr, value in data.items():
            setattr(plant, attr, value)

        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return make_response({"error": "Plant not found"}, 404)

        db.session.delete(plant)
        db.session.commit()
        return make_response('', 204)


# Register routes
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
