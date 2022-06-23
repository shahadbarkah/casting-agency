# Casting Agency
### About
The project is API for a casting company that is responsible for creating and managing and assigning actors to those movies.
###### URL for API hosted on Heroku:
[ca casting agency](https://ca-casting-agency.herokuapp.com/)

#### Roles and Permissions:

##### Casting Assistant
User with casting assistance assigned role has the following permissions:
- get:actors
- get:movies

##### Casting Director
User with casting director assigned role has the following permissions:
- all casting assistance permissions.
- post:actors
- post:movie-actors
- post:actor-movies
- patch:actors
- patch:movies
- delete:actors

##### Executive Producer
User with executive producer assigned role has the following permissions:
- all casting director permissions.
- post:movies
- delete:movies

### Installing Dependencies

1. **Python**  
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Environment** 
It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** 
Once you have your virtual environment setup and running, install dependencies running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM. It will be used to handle the PostgreSQL database.

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension that will be used to handle cross-origin requests from the frontend server. 


### Database Setup
With Postgres running, create a database for your app and a database for testing using the command below, update the setup.sh file with your databases name:
```bash
createdb databasename
```

### Running the server

Ensure you are working using your created virtual environment. To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development # enables debug mode
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

 

## API Reference
### Endpoints
##### GET /login
Redirect the user to login page.
##### GET /movies
- Retrieve a list of all movies and a success value.
- Request Arguments: None
- Required permissions: get:actors
- Sample: `curl -X GET https://ca-casting-agency.herokuapp.com/movies -H "authorization: Bearer <TOKEN>"`
##### GET /actors
- Retrieve a list of all actors and a success value.
- Request Arguments: None
- Required permissions: get:movies
- Sample: `curl -X GET https://ca-casting-agency.herokuapp.com/actors -H "authorization: Bearer <TOKEN>"`
##### GET /movies/<int:movie_id>
- Retrieve the movie of the given id if it exists, list of all the actors associated with the movie and a success value.
- Request Arguments: None
- Required permissions: get:movies
- Sample: `curl -X GET https://ca-casting-agency.herokuapp.com/movies/1 -H "authorization: Bearer <TOKEN>"`
##### GET /actors/<int:actor_id>
- Retrieve the actor of the given id if it exists, list of all the movies associated with the actor and success value.
- Request Arguments: None
- Required permissions: get:actors
- Sample: `curl -X GET https://ca-casting-agency.herokuapp.com/actors/4 -H "authorization: Bearer <TOKEN>" `
##### POST /actors
- Create a new actor.
- Request Arguments: name, age, gender, image_link, twitter_link(optional), instgram_link(optional), facebook_link(optional) of the new actor.
- Required permissions: post:actors
- Returns: actor object and a success value.
- Sample: `curl -X POST https://ca-casting-agency.herokuapp.com/actors -H "authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"name\":\"nena\",\"age\":\"30\",\"gender\":\"female\",\"image_link\":\"iamge.com\"}"`
##### POST /movies
- Create a new movie.
- Request Arguments: title, poster and release_date.
- Required permissions: post:movies
- Returns: movie object and a success value.
- Sample: `curl -X POST https://ca-casting-agency.herokuapp.com/movies -H "authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d  "{\"title\":\"The blue\", \"poster\":\"http.poster.com\",\"release_date\":\"2024-11-3\"}"`
##### POST /actors/<int:actor_id>
- Create actor movies list of the given id if it exists.
- Request Arguments: list of movie_id
- Required permissions: post:actor-movies
- Returns: actor object , list of actor movies and a success value.
- Sample:  `curl -X POST https://ca-casting-agency.herokuapp.com/actors/4 -H "authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"movie_id\":[1,6]}"`
##### POST /movies/<int:movies_id>
- Create actors list of the movie .
- Request Arguments: list of actor_id
- Required permissions: post:movie-actors
- Returns: movie object, list of movie actors and a success value.
- Sample: `curl -X POST https://ca-casting-agency.herokuapp.com/movies/1 -H "authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"actor_id\":[9]}"`
##### PATCH /actors/<int:actor_id>
- Edit actor data of the given id if it exists.
- Request Arguments: the data need to edit which may be name, age, gender, image_link, twitter_link, instgram_link or facebook_link
- Required permissions: patch:actors
- Returns: actor object and a success value.
- Sample: `curl -X PATCH https://ca-casting-agency.herokuapp.com/actors/4 -H "authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"name\":\"nana\",\"age\":\"32\"}"`
##### PATCH /movies/<int:movies_id>
- Edit movie data of the given id if it exists.
- Request Arguments: the data need to edit which may be title, poster or release_date
- Required permissions: patch:movies
- Returns: movie object and a success value.
- Sample:  `curl -X PATCH https://ca-casting-agency.herokuapp.com/movies/1 -H "authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d  "{\"release_date\":\"2025-9-3\"}"`
##### DELETE /actors/<int:actor_id>
- Delete actor of the given id if it exists.
- Request Arguments: None
- Required permissions: delete:actors
- Returns: deleted actor id and a success value.
- Sample: `curl -X DELETE https://ca-casting-agency.herokuapp.com/actors/7 -H "authorization: Bearer <TOKEN>"`
##### DELETE /movies/<int:movies_id>
- Delete movie of the given id if it exists.
- Request Arguments: None
- Required permissions: delete:movies
- Returns: deleted movie id and a success value.
- Sample: `curl -X DELETE https://ca-casting-agency.herokuapp.com/movies/7 -H "authorization: Bearer <TOKEN>"`

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return the following errors types when requests fail:
- 400: Bad Request
- 403: unauthorized
- 404: Resource Not Found
- 405: Method not allowed
- 422: unprocessable
- 500: internal server error
- 422: Not Processable 

## Testing
Create test database, change TEST_DB_NAME variable in setup.sh to the name of the database you have created. Run the tests using the following command:
```
python test_app.py
```