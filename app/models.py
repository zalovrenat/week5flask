from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(45),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    date_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

class Pokedex(db.Model):
    pokedex_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,unique=True)

    def __init__(self, user_id):
        self.user_id = user_id

class PokedexPokemon(db.Model):
    pokedex_pokemon_id = db.Column(db.Integer,primary_key=True)
    pokedex_id = db.Column(db.Integer,db.ForeignKey('pokedex.pokedex_id'),nullable=False)
    pokemon_id = db.Column(db.Integer,db.ForeignKey('pokemon.pokemon_id'),nullable=False)

    def __init__(self, pokedex_id, pokemon_id):
        self.pokedex_id = pokedex_id
        self.pokemon_id = pokemon_id

class Pool(db.Model):
    pool_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,unique=True)

    def __init__(self, user_id):
        self.user_id = user_id

class PoolPokemon(db.Model):
    pool_pokemon_id = db.Column(db.Integer,primary_key=True)
    pool_id = db.Column(db.Integer,db.ForeignKey('pool.pool_id'),nullable=False)
    pokemon_id = db.Column(db.Integer,db.ForeignKey('pokemon.pokemon_id'),nullable=False)

    def __init__(self, pool_id, pokemon_id):
        self.pool_id = pool_id
        self.pokemon_id = pokemon_id

class Pokemon(db.Model):
    pokemon_id = db.Column(db.Integer,primary_key=True)
    pokemon_name = db.Column(db.String(25),nullable=False)
    img_url = db.Column(db.String,nullable=False)
    ability1 = db.Column(db.String(50),default='')
    ability2 = db.Column(db.String(50),default='')
    base_xp = db.Column(db.Integer,nullable=False,default=0)
    hp_base_stat = db.Column(db.Integer,nullable=False,default=0)
    attack_base_stat = db.Column(db.Integer,nullable=False,default=0)
    defense_base_stat = db.Column(db.Integer,nullable=False,default=0)

    def __init__(self,pokemon_id,pokemon_name,img_url,ability1,ability2,base_xp,hp_base_stat,attack_base_stat,defense_base_stat):
        self.pokemon_id = pokemon_id
        self.pokemon_name = pokemon_name
        self.img_url = img_url
        self.ability1 = ability1
        self.ability2 = ability2
        self.base_xp = base_xp
        self.hp_base_stat = hp_base_stat
        self.attack_base_stat = attack_base_stat
        self.defense_base_stat = defense_base_stat

class Team(db.Model):
    team_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,unique=True)
    pokemon_id = db.Column(db.Integer,db.ForeignKey('pokemon.pokemon_id'),nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id