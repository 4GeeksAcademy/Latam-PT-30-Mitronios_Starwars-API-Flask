"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Defining Get Method

# Get Users
@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    if len(users) <1:
        return jsonify({"Message": "No users exists"}), 404
    serializing = list(map(lambda x: x.serialize(), users))
    return jsonify(serializing), 200


# Get Planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    if len(planets) <1:
        return jsonify({"Message": "No planet exists"}), 404
    serializing_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(serializing_planets), 200


# Get Characters
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    if len(characters) <1:
        return jsonify({"Message": "No character exists"}), 404
    serializing_characters = list(map(lambda x: x.serialize(), characters))
    return jsonify(serializing_characters), 200


# Get user by ID
@app.route('/user/<int:user_id>', methods = ['GET'])
def get_one_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"Message": "User not found"}), 404
    serialize_user = user.serialize()
    return jsonify(serialize_user)


# Get Planet by ID
@app.route('/planets/<int:planet_id>', methods = ['GET'])
def get_one_planet(planet_id):
    planet= Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"Message": "Planet not found"}), 404
    serialize_planet = planet.serialize()
    return serialize_planet


# Get Chatacter by ID
@app.route('/characters/<int:character_id>', methods = ['GET'])
def get_one_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"Message": "Character not found"}), 404
    serialize_character = character.serialize()
    return serialize_character


#  Get Favorites
@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Character.query.all()
    if len(favorites) <1:
        return jsonify({"Message": "No favorites added"}), 404
    serializing_favorites= list(map(lambda x: x.serialize(), favorites))
    return serializing_favorites, 200

# Get User's Favorites
@app.route('/user/<int:user_id>/favorites', methods = ['GET'])
def get_user_favorites(user_id):
    user_exists = User.query.get(user_id)
    if user_exists is None:
        return jsonify({"Message": "User doesn't exists"}), 404
    serialize_user_favorites = list(map(lambda x: x.serialize(), user_exists.favorites))
    if len(serialize_user_favorites) <1:
        return jsonify({"Message": "No Favorites added"})
    return jsonify(serialize_user_favorites)


# Defining Post Methods

# Post Favorite Planet

@app.route('/favorite/planet/<int:planet_id>', methods = ['POST'])
def add_favorite_planet(planet_id):
    user_id = 1 
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    
    if planet is None:
        return jsonify({"Message": "Planet not found"}), 404

    if any(fav.planet_id == planet_id for fav in user.favorites):
        return jsonify({"Message": "Planet already in favorites"}), 400

    new_favorite = Favorite(user_id=user.id, planet_id=planet.id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"Message": "Fav Planet Added"}), 201

# Post Favorite character

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = 1
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    
    if character is None:
        return jsonify({"Message": "Character not found"}), 404

    if any(fav.character_id == character_id for fav in user.favorites):
        return jsonify({"Message": "Character already in favorites"}), 400

    new_favorite = Favorite(user_id=user.id, character_id=character.id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"Message": "Fav character Added"}), 201

# Defining DELETE Methods

# Delete Fav Planet

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1
    user = User.query.get(user_id)
    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()

    if favorite is None:
        return jsonify({"Message": "Favorite planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"Message": "Planet Removed from Fav"}), 200

# Delete Fav Character
@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    user_id = 1
    user = User.query.get(user_id)
    favorite = Favorite.query.filter_by(user_id=user.id, character_id=character_id).first()

    if favorite is None:
        return jsonify({"Message": "Favorite character not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"Message": "Character removed from Fav"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)





