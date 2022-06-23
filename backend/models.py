import os
from re import S
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import json

database_name = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database_path = os.getenv('DATABASE_URL', "postgresql://{}:{}@{}/{}".format(username, password,
                                                  host, database_name))
if database_path.startswith('postgres://'):
    database_path = database_path.replace('postgres://', 'postgresql://',1)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.drop_all()
    db.create_all()


'''
movie_actor association table

'''

movie_actor = db.Table("movie_actor",
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id', ondelete='CASCADE'))
)


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actor'
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String, nullable=False)
    twitter_link = db.Column(db.String(120))
    instgram_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    

    def __init__(self, name, age, gender, image_link, twitter_link="", instgram_link="",facebook_link=""):
        self.name = name
        self.age = age
        self.gender = gender
        self.image_link = image_link
        self.twitter_link = twitter_link
        self.instgram_link = instgram_link
        self.facebook_link = facebook_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'image_link': self.image_link,
            'twitter_link': self.twitter_link,
            'instgram_link': self.image_link,
            'facebook_link': self.facebook_link
            }


'''
Movie

'''


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    poster = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    actor = db.relationship('Actor', secondary=movie_actor, backref='movies', lazy='joined')

    def __init__(self, title, poster, release_date):
        self.title = title
        self.poster = poster
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'poster': self.poster,
            'release_date': self.release_date,
            }
