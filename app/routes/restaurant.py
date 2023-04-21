from flask import Blueprint, jsonify

class Restaurant:
    def __init__(self, id, rating, name, cuisine, distance_from_ada):
        self.id = id
        self.rating = rating
        self.name = name
        self.cuisine = cuisine
        self.distance_from_ada = distance_from_ada

restaurant1 = Restaurant(1, 5, "Pizza Hut", "Italian", 3.6)
restaurant2 = Restaurant(15, 2, "Dominos", "American", 0.2)
restaurant3 = Restaurant(9, 4.5, "Hong Kong Bistro", "Chinese", 0.1)

restaurant_list = [restaurant1, restaurant2, restaurant3]

restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/restaurant")

@restaurant_bp.route("", methods=["GET"])
def get_restaurants():
    response = []
    for restaurant in restaurant_list:
        restaurant_dict = {
            "id": restaurant.id,
            "rating": restaurant.rating,
            "name": restaurant.name,
            "cuisine": restaurant.cuisine,
            "distance_from_ada": restaurant.distance_from_ada
        }
        response.append(restaurant_dict)

    return jsonify(response), 200

#/restaurant/<id>
@restaurant_bp.route("/<id>", methods=["GET"])
def get_one_restaurant(id):
    try:
        restaurant_id = int(id)
    except ValueError:
        return {"message": f"invalid id: {id}"}, 400

    for restaurant in restaurant_list:
        if restaurant.id == restaurant_id:
            return jsonify({
                "id": restaurant.id,
                "nested_example": {"hey": "hi"},
                "rating": restaurant.rating,
                "name": restaurant.name,
                "cuisine": restaurant.cuisine,
                "distance_from_ada": restaurant.distance_from_ada
            }), 200
        
    return {"message": f"id {restaurant_id} not found"}, 404
