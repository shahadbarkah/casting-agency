import os
from re import A
from typing import AsyncGenerator
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth
import sys


DOMAIN = os.getenv('AUTH0_DOMAIN')
API_IDENTIFIER = os.getenv('API_AUDIENCE')
CLIENT_ID = os.getenv('CLIENT_ID')
URI = os.getenv('REDIRECT_URI')
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, authorization, true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')

        return response

  
    @app.route('/')
    def get_greeting():
        return jsonify({
            'success': True,
            "greeting": "wolcome to ca casting agency :)"
        }, 200)


    @app.route('/login')
    def redirect_login():
        login_url = f'https://{DOMAIN}/authorize?audience={API_IDENTIFIER}&response_type=token&client_id={CLIENT_ID}&redirect_uri={URI}'
        return redirect(login_url)


    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        if payload == AuthError:
            abort(payload.status_code)

        actors = Actor.query.all()
        if actors:
            return jsonify({
                "success": True,
                "actors": [actor.format() for actor in actors]
            }, 200)

        abort(404)
 

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        if payload == AuthError:
            abort(payload.staus_code)

        movies = Movie.query.all()
        if movies:
            return jsonify({
                "success": True,
                "movies": [movie.format() for movie in movies]
            }, 200)
        abort(404)
        

    @app.route('/actors/<int:actor_id>')
    @requires_auth('get:actors')
    def get_actor_movies(payload, actor_id):
        if payload == AuthError:
            abort(payload.status_code)

        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor:
            movies = Movie.query.filter(Movie.actor.any(id=actor_id)).all()
            if movies:
                movies = [movie.format() for movie in movies]
            return jsonify({
                "success": True,
                "actor": actor.format(),
                "movies": movies
            }, 200)
        abort(404)


    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def get_movie_actors(payload, movie_id):
        if payload == AuthError:
            abort(payload.status_code)

        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie:
            actors = Actor.query.filter(Actor.movies.any(id=movie_id)).all()
            if actors:
                actors = [actor.format() for actor in actors]
            return jsonify({
                "success": True,
                "movie": movie.format(),
                "actors": actors
            }, 200)
        abort(404)

    @app.route('/actors/<int:actor_id>', methods=['POST'])
    @requires_auth('post:actor-movies')
    def add_actor_movies(payload, actor_id):
        if payload == AuthError:
            abort(payload.status_code)
        
        body = request.get_json()
        movie_ids = body.get('movie_id', None)
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor:
            movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()
            if len(movies) == 0:
                abort(404)
            actor.movies = [movie for movie in movies]
            actor.update()
            movies = Movie.query.filter(Movie.actor.any(id=actor_id)).all()
            movies = [movie.format() for movie in movies]
            return jsonify({
                "success": True,
                "actor": actor.format(),
                "movies": movies
            }, 200)
        abort(404)


    @app.route('/movies/<int:movie_id>', methods=['POST'])
    @requires_auth('post:movie-actors')
    def add_movie_actors(payload, movie_id):
        if payload == AuthError:
            abort(payload.status_code)

        body = request.get_json()
        actor_ids = body.get('actor_id', None)
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie:
            actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()
            if len(actors) == 0:
                abort(404)

            movie.actor = [actor for actor in actors]
            movie.update()
            actors = Actor.query.filter(Actor.movies.any(id=movie_id)).all()
            actors = [actor.format() for actor in actors]
            return jsonify({
                "success": True,
                "movie": movie.format(),
                "actors": actors
            }, 200)
        abort(404)
    

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        if payload == AuthError:
            abort(payload.status_code)
        
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor:
            actor.delete()
            return jsonify({
                "success": True,
                "delete_id": actor_id
            }, 200)
        abort(404)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        if payload == AuthError:
            abort(payload.status_code)

        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie:
            movie.delete()
            return jsonify({
                "success": True,
                "delete_id": movie_id
            }, 200)
        abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        if payload == AuthError:
            abort(payload.status_code)
        try:
            body = request.get_json()
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            image_link = body.get('image_link', None)
            twitter_link = body.get('twitter_link', None)
            instgram_link = body.get('instgram_link', None)
            facebook_link = body.get('facebook_link', None)
            actor = Actor(name, age, gender, image_link,
                          twitter_link, instgram_link, facebook_link)
            actor.insert()
            return jsonify({
                "success": True,
                "actor": actor.format()
            }, 200)
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        if payload == AuthError:
            abort(payload.status_code)
        try:
            body = request.get_json()
            title = body.get('title', None)
            poster = body.get('poster', None)
            release_date = body.get('release_date', None)
            movie = Movie(title, poster, release_date)
            movie.insert()
            return jsonify({
                "success": True,
                "movie": movie.format()
            }, 200)
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        if payload == AuthError:
            abort(payload.status_code)
        
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        image_link = body.get('image_link', None)
        twitter_link = body.get('twitter_link', None)
        instgram_link = body.get('instgram_link', None)
        facebook_link = body.get('facebook_link', None)
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor :
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender
            if image_link:
                actor.image_link = image_link
            if twitter_link:
                actor.twitter_link = twitter_link
            if instgram_link:
                actor.instgram_link = instgram_link
            if facebook_link:
                actor.facebook_link = facebook_link
            actor.update()
            return jsonify({
            "success": True,
            "actor": actor.format()
            }, 200)
        abort(404)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        if payload == AuthError:
            abort(payload.status_code)

        body = request.get_json()
        title = body.get('title', None)
        poster = body.get('poster', None)
        release_date = body.get('release_date', None)
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie:
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date
            if poster:
                movie.poster = poster
            movie.update()
            return jsonify({
                "success": True,
                "movie": movie.format()
            }, 200)
        abort(404)


    '''
    Error handlers for all expected errors
 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resourse not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
      }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['code'],
            "description": error.error['description']
        }), error.status_code


    return app

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
