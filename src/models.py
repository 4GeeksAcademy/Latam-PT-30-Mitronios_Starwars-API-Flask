from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tableName__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # Relationship with Favorite
    favorites = db.relationship("Favorite", back_populates = "user")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }



class Favorite(db.Model):
    __tablename__ = "favorite"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    character_id = db.Column(db.Integer)
    planet_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }
    
    # Relationship with User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates = "favorites")

    # Relationship with Character
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    character = db.relationship("Character", back_populates = "favorites")

    # Relationship with Planet
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship("Planet", back_populates = "favorites")

class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(350))
    specimen = db.Column(db.String(350))
    height_cm = db.Column(db.String(10))
    eye_color = db.Column(db.String(10))
    class_order = db.Column (db.String(50))

    # Relationship with Favorite
    favorites = db.relationship("Favorite", back_populates = "character")

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "specimen": self.specimen,
            "height_cm": self.height_cm,
            "eye_color": self.eye_color,
            "class_order": self.class_order,
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.Integer)
    atmosphere = db.Column(db.Integer)
    native_creatures = db.Column(db.String(500))
    capital = db.Column(db.String(250))

    # Relationship with Favorite
    favorites = db.relationship("Favorite", back_populates = "planet")

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "atmosphere": self.atmosphere,
            "native_creatures": self.native_creatures,
            "capital": self.capital,
        }
