import unittest
import json
import os

from werkzeug.test import Client
from app import create_app
from models import setup_db, Actor, Movie, db

casting_assistant_JWT = os.getenv('CASTING_ASSISTANT_JWT')
casting_director_JWT = os.getenv('CASTING_DIRECTOR_JWT')
executive_producer_JWT = os.getenv('EXECUTIVE_PRODUCER_JWT')
expire_token = os.getenv('EXPIRE_TOKEN')
invalid_token = os.getenv('INVALID_TOKEN')

class castingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv('TEST_DB_NAME')
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.username, self.password,
                                                        self.host, self.database_name)
        setup_db(self.app, self.database_path)


        self.new_actor = {
            "name": "Nena",
            "age": "20",
            "gender": "female",
            "image_link": "https://cdn.pixabay.com/photo/2021/12/24/08/41/woman-6890711_960_720.jpg"
        }

        self.new_movie = {
            "title": "blue between us",
            "poster": "https://cdn.pixabay.com/photo/2021/12/24/08/41/woman-6890711_960_720.jpg",
            "release_date": "2021-11-3"
        }

        self.update_actor = {
            "age": "50",
            "name": "Jane"
        }

        self.update_movie = {
            "title": "the earth",
            "release_date": "2023-10-11"
        }
        self.image = "https://cdn.pixabay.com/photo/2021/12/24/08/41/woman-6890711_960_720.jpg"


    """
    Test for successful operation and for expected errors.
    """

    def test_get_actors(self):
        new_actor = Actor(name="seong", age=22, gender='male', image_link=self.image)
        new_actor.insert()
        res = self.client().get('/actors', headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['actors'])
    
    def test_get_actors_error_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'authorization_header_missing')
    
    def test_get_movies(self):
        new_movie = Movie(title='sibel',poster=self.image, release_date='2020-11-23')
        new_movie.insert()
        res = self.client().get('/movies', headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['movies'])
    
    def test_get_movies_error_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'authorization_header_missing')
    
    def test_get_actor_movies(self):
        new_actor = Actor(name="seong", age=22, gender='male', image_link=self.image)
        new_actor.insert()
        res = self.client().get(f'/actors/{new_actor.id}', headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['actor'])

    def test_get_actor_movies_error_401(self):
        res = self.client().get('/actors/900000', headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resourse not found')

    def test_get_movie_actors(self):
        new_movie = Movie(title='sibel',poster=self.image , release_date='2020-11-23')
        new_movie.insert()
        res = self.client().get(f'/movies/{new_movie.id}', headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['movie'])
    
    def test_get_movie_actors_error_404(self):
        res = self.client().get('/movies/900000', headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resourse not found')
    
    def test_add_actor_movies(self):
        new_actor = Actor(name='lolo', age=33, gender='female', image_link=self.image)
        new_movie = Movie(title="the sky",poster=self.image, release_date='2022-10-9')
        new_actor.insert()
        new_movie.insert()
        res = self.client().post(f'actors/{new_actor.id}', headers={"Authorization": casting_director_JWT},
                                 json={"movie_id": [new_movie.id]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['actor'])
        self.assertTrue(data[0]['movies'])
    
    def test_add_actor_movies_error_403(self):
        new_actor = Actor(name='lolo', age=33, gender='female', image_link=self.image)
        new_movie = Movie(title="the sky", poster=self.image, release_date='2022-10-9')
        new_actor.insert()
        new_movie.insert()
        res = self.client().post(f'actors/{new_actor.id}', headers={"Authorization": casting_assistant_JWT},
                                 json={"movie_id": [new_movie.id]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unauthorized")
    
    def test_add_movie_actors(self):
        new_actor = Actor(name='lolo', age=33, gender='female', image_link=self.image)
        new_movie = Movie(title="the sky", poster=self.image, release_date='2022-10-9')
        new_actor.insert()
        new_movie.insert()
        res = self.client().post(f'movies/{new_movie.id}', headers={"Authorization": casting_director_JWT},
                                 json={"actor_id": [new_actor.id]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['movie'])
        self.assertTrue(data[0]['actors'])
    
    def test_add_actor_movies_error_403(self):
        new_actor = Actor(name='lolo', age=33, gender='female', image_link=self.image)
        new_movie = Movie(title="the sky", poster=self.image, release_date='2022-10-9')
        new_actor.insert()
        new_movie.insert()
        res = self.client().post(f'movies/{new_movie.id}', headers={"Authorization": casting_assistant_JWT},
                                 json={"movie_id": [new_actor.id]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unauthorized")
    
    def test_delete_actor(self):
        new_actor = Actor(name='lisa', age=33, gender='female', image_link=self.image)
        new_actor.insert()
        res = self.client().delete(f'/actors/{new_actor.id}', headers={"Authorization": casting_director_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertEqual(data[0]['delete_id'], new_actor.id)
    
    def test_delete_actor_error_403(self):
        new_actor = Actor(name='lisa', age=33, gender='female',image_link=self.image)
        new_actor.insert()
        res = self.client().delete(f'/actors/{new_actor.id}', headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unauthorized")

    def test_delete_actor_error_404(self):
        res = self.client().delete(f'/actors/9090909', headers={"Authorization": casting_director_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resourse not found')

    def test_delete_movie(self):
        new_movie = Movie(title='sibel', poster=self.image, release_date='2020-11-23')
        new_movie.insert()

        res = self.client().delete(f'/movies/{new_movie.id}', headers={"Authorization": executive_producer_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['success'], True)
        self.assertEqual(data[0]['delete_id'], new_movie.id)

    def test_delete_movie_error_403(self):
        new_movie = Movie(title='sibel', poster=self.image, release_date='2020-11-23')
        new_movie.insert()

        res = self.client().delete(f'/movies/{new_movie.id}', headers={"Authorization": casting_director_JWT})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unauthorized")

    def test_delete_movie_error_404(self):
        res = self.client().delete(f'/movies/9090909', headers={"Authorization": executive_producer_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resourse not found')

    def test_add_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": casting_director_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['actor'])

    def test_add_actor_error_403(self):
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unauthorized")

    def test_add_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": executive_producer_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['movie'])

    def test_add_actor_error_403(self):
        res = self.client().post('/movies', json=self.new_actor, headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unauthorized")

    def test_update_actor(self):
        new_actor = Actor(name='lisa', age=33, gender='female', image_link=self.image)
        new_actor.insert()
        res = self.client().patch(f'/actors/{new_actor.id}', json=self.update_actor, headers={"Authorization": casting_director_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['actor'])
    
    def test_update_actor_error_403(self):
        new_actor = Actor(name='lisa', age=33, gender='female', image_link=self.image)
        new_actor.insert()
        res = self.client().patch(f'/actors/{new_actor.id}', json=self.update_actor, headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unauthorized")

    def test_update_actor_error_404(self):
        res = self.client().patch('/actors/5042033', json=self.update_actor, headers={"Authorization": casting_director_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resourse not found')

    def test_update_movie(self):
        new_movie = Movie(title='sibel', poster=self.image, release_date='2020-11-23')
        new_movie.insert()
        res = self.client().patch(f'/movies/{new_movie.id}', json=self.update_movie, headers={"Authorization": casting_director_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]['success'])
        self.assertTrue(data[0]['movie'])

    def test_update_movie_error_403(self):
        new_movie = Movie(title='sibel', poster=self.image, release_date='2020-11-23')
        new_movie.insert()

        res = self.client().patch(f'/movies/{new_movie.id}', json=self.update_movie, headers={"Authorization": casting_assistant_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unauthorized")

    def test_update_movie_error_404(self):
        res = self.client().patch('/movies/220202223', json=self.update_movie, headers={"Authorization": casting_director_JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resourse not found')

    def test_expire_token_error_401(self):
        res = self.client().get(
            '/actors', headers={"Authorization": expire_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'token_expired')


    def test_invalid_token_error_401(self):
        res = self.client().get(
            '/actors', headers={"Authorization": invalid_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'invalid_header')
    

    def test_no_authorization_header_error_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'authorization_header_missing')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()