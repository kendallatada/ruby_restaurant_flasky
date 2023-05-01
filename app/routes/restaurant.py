from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.restaurant import Restaurant

restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")

@restaurant_bp.route("", methods=["POST"])
def add_restaurant():
    request_body = request.get_json()
    new_restaurant = Restaurant(
        rating = request_body["rating"],
        name = request_body["name"],
        cuisine = request_body["cuisine"],
        distance_from_ada = request_body["distance_from_ada"]
    )

    db.session.add(new_restaurant)
    db.session.commit()

    return {"id": new_restaurant.id}, 201

@restaurant_bp.route("", methods=["GET"])
def get_restaurants():
    response = []
    all_restaurants = Restaurant.query.all()
    for restaurant in all_restaurants:
        response.append(restaurant.to_dict())

    return jsonify(response), 200

#/restaurant/<id>
@restaurant_bp.route("/<rest_id>", methods=["GET"])
def get_one_restaurant(rest_id):
    restaurant = validate_restaurant(rest_id)

    # if restaurant is None:
    #     return {"message": f"id {restaurant_id} not found"}, 404
    
    return restaurant.to_dict(), 200


@restaurant_bp.route("/<rest_id>", methods=["PUT"])
def update_restaurant(rest_id):
    restaurant = validate_restaurant(rest_id)

    request_data = request.get_json()

    restaurant.name = request_data["name"]
    restaurant.cuisine = request_data["cuisine"]
    restaurant.rating = request_data["rating"]
    restaurant.distance_from_ada = request_data["distance_from_ada"]

    db.session.commit()

    return {"msg": f"restaurant {rest_id} successfully updated"}, 200


@restaurant_bp.route("/<rest_id>", methods=["DELETE"])
def delete_restaurant(rest_id):
    restaurant = validate_restaurant(rest_id)

    db.session.delete(restaurant)
    db.session.commit()

    return {"msg": f"restaurant {rest_id} successfully deleted"}, 200


def validate_restaurant(rest_id):
    try:
        restaurant_id = int(rest_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {rest_id}"}, 400))
    
    return Restaurant.query.get_or_404(restaurant_id)


