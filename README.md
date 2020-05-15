# Endorsa

## Index of contents
- [Intro](##Intro)
- [Motivation](##Motivation)
- [Local set up](##local-set-up)
- [Roled-Based Access Control (RBAC)](##Roled-Based-Access-Control-(RBAC))
- [API endpoints](##API-endpoints)
- [Testing](##Testing)

## Intro

This is a capstone project for the Udacity Full-Stack Web Developer Nanodegree program. More info about this course [here](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

This repository includes a Flask API backed by a PostgreSQL database and Auth0 role-based access control. The API is now hosted in Heroku and it can be also set up and run in your local machine. The link to the app in Heroku us the following:

```bash
https://endorsa-network.herokuapp.com/
```

Currently, there is no front-end developed for the application.

Here is a list and short description of the files contained in the repository:
- [app.py](/app.py) - run API server with Flask
- [models.py](/models.py) - database models and table relationships with SQLAlchemy
- [test_app.py](/test_app.py) - API local testing using Unittest
- [endorsa_api_testing.postman_collection.json](/endorsa_api_testing.postman_collection.json) - Postman collection for API local and remote testing
- [auth.py](/auth.py) - JWT authentication with Auth0
- [manage.py](/manage.py) - run database migrations
- [config.ini](/config.ini) - token variables
- [requirements.txt](/requirements.txt) - Python packages required
- [setup.sh](/setup.sh) - environment variables required
- [Procfile](/config.ini) - configuration file for Gunicorn app in Heroku
- [migrations](/migrations) - database migrations record


## Motivation
Endorsa is a social network for exclusive professional networking based on trustful relationships.

In real-life professional networking, trustful relationships usually outweigh CVs and other self-promoting techniques. What others say about us right now matter more to others, that what we say about ourselves about our past achievements. Validation and references from others we trust becomes even more relevant, probably the most important factor, when taking high-stakes executive decisions for hiring, contracting or advicing.

Current professional social networks, on the other hand, focus more on self-promotion and online CVs which usually are not peer-reviewed, leading to an overflow of low quality, unreliable data on who to make business with.

Endorsa is a new exclusive social network focused on professional trustful relationships and accountability where people can state who do they trust the most for a given skill, as well as promote themselves solely by what others say about their strengths.

## Local set up

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the project directory and running:

```bash
pip install -r requirements.txt
```

### Database Setup
In order to run the code locally, it is required to create a PostgreSQL database. One easy way to do this is to [install](https://www.postgresql.org/download/) PostgreSQL and run in your terminal:
```
createdb endorsa
```
Once created the database, remember to update the environment variable set in [setup.sh](/setup.sh) with your own local database URL. Or create the environment variable directly in your terminal.

### Running the server

To run the server, execute:

```bash
python app.py
```

You can test it locally in:
```
http://localhost:5000/
```

### Error handling
Errors are returned as JSON objects in the following format:
```python
{
    'success': False,
    'error': 404,
    'message': 'Resource not found'
}
```

The API will return 2 error types when request fails:
- 404: Resource Not Nound
- 422: Unprocessable
- 401: Authorization error

## Roled-Based Access Control (RBAC)

A RBAC authentication system based on JSON Web Tokens (JWTs) has been set up using [Auth0 service](https://auth0.com/).

There are 2 roles defined:
- Admin: read and write rights.
- User: only read rights.

The permissions defined are the following:
- read:users
- edit:users
- read:skills
- edit:skills
- read:endorsements
- edit:endorsements

In order to get access to the API endpoint, you must include the required token in the request header as the following:
```
Authorization: Bearer <token>
```

Right now there is not an available log in page to get a token automatically. Tokens must be provided manually and expire after 30 days.

More on JSON Web Tokens [here](https://auth0.com/learn/json-web-tokens/).

## API endpoints

The application contains the following API endpoints.

### GET /users
- General:
    - Returns a list of users, success value and number of users
    - User rights required

- Output sample: 

```bash
{
  "num_users": 1,
  "success": true,
  "users": [
    {
      "contact": 123456789,
      "description": "Freelance Gangster | MBA",
      "first_name": "Vincent",
      "id": 101,
      "last_name": "Vega",
      "location": "California"
    }
  ]
}
```

### DELETE /users
- General:
    - Deletes all users in the database
    - Returns success value and number of users deleted
    - Admin rights required

- Output sample: 

```bash
{
  "num_users_deleted": 1,
  "success": true
}
```

### POST /users
- General:
    - Creates a new user using the submitted user profile in JSON format. Fields first_name and last_name are required
    - Returns success value and new user basic info
    - Admin rights required

- Input sample:
```bash
{
    "first_name": "Vincent",
    "last_name": "Vega",
    "location": "California",
    "description": "Freelance Gangster | MBA",
    "contact": "123456789"
}
```

- Output sample: 

```bash
{
  "success": true,
  "user": {
    "contact": 123456789,
    "description": "Freelance Gangster | MBA",
    "first_name": "Vincent",
    "id": 104,
    "last_name": "Vega",
    "location": "California"
  }
}
```

### GET /users/{user_id}
- General:
    - Returns detailed info of user with the given ID, including information about endorsements received and given
    - User rights required

- Output sample: 

```bash
{
  "endorsements_given": [
    {
      "creation_date": "Fri, 15 May 2020 00:00:00 GMT",
      "first_name": "Vincent",
      "last_name": "Vega",
      "name": "Problem solving",
      "receiver_id": 104,
      "skill_id": 47
    }
  ],
  "endorsements_received": [
    {
      "creation_date": "Fri, 15 May 2020 00:00:00 GMT",
      "first_name": "Vincent",
      "giver_id": 104,
      "last_name": "Vega",
      "name": "Problem solving",
      "skill_id": 47
    }
  ],
  "success": true,
  "user": {
    "contact": 123456789,
    "description": "Freelance Gangster | MBA",
    "first_name": "Vincent",
    "id": 104,
    "last_name": "Vega",
    "location": "California"
  }
}
```

### PATCH /users/{user_id}
- General:
    - Updates submitted info of user with the given ID
    - Returns success value and new user basic info
    - Admin rights required

- Input sample:
```bash
{
    "location": "New York",
    "description": "Senior Gangster | MBA"
}
```

- Output sample: 

```bash
{
  "success": true,
  "user": {
    "contact": 123456789,
    "description": "Senior Gangster | MBA",
    "first_name": "Vincent",
    "id": 104,
    "last_name": "Vega",
    "location": "New York"
  }
}
```

### DELETE /users/{user_id}
- General:
    - Deletes user with the given ID
    - Returns success value and deleted user basic info
    - Admin rights required

- Output sample: 

```bash
{
  "success": true,
  "user": {
    "contact": 123456789,
    "description": "Senior Gangster | MBA",
    "first_name": "Vincent",
    "id": 104,
    "last_name": "Vega",
    "location": "New York"
  }
}
```

### GET /skills
- General:
    - Returns a list of skills, success value and number of skills
    - User rights required

- Output sample: 

```bash
{
  "num_skills": 1,
  "skills": [
    {
      "description": "Ability to deal with complex situations and come up with a solution",
      "id": 49,
      "name": "Problem solving"
    }
  ],
  "success": true
}
```

### DELETE /skills
- General:
    - Deletes all skills in the database
    - Returns success value and number of skills deleted
    - Admin rights required

- Output sample: 

```bash
{
  "num_skills_deleted": 1,
  "success": true
}
```

### POST /skills
- General:
    - Creates a new skill using the submitted skill profile in JSON format. Field name is required
    - Returns success value and new skill basic info
    - Admin rights required

- Input sample:
```bash
{
    "name": "Problem solving",
    "description": "Ability to deal with complex situations and come up with a solution"
}
```

- Output sample: 

```bash
{
  "skill": {
    "description": "Ability to deal with complex situations and come up with a solution",
    "id": 50,
    "name": "Problem solving"
  },
  "success": true
}
```

### GET /skills/{skill_id}
- General:
    - Returns detailed info of skill with the given ID, including information about endorsements received and given for that given skill
    - User rights required

- Output sample: 

```bash
{
  "endorsements": [
    {
      "creation_date": "Fri, 15 May 2020 00:00:00 GMT",
      "giver_first_name": "Vincent",
      "giver_id": 105,
      "giver_last_name": "Vega",
      "receiver_first_name": "Vincent",
      "receiver_id": 105,
      "receiver_last_name": "Vega"
    }
  ],
  "skill": {
    "description": "Ability to deal with complex situations and come up with a solution",
    "id": 50,
    "name": "Problem solving"
  },
  "success": true
}
```

### PATCH /skills/{skill_id}
- General:
    - Updates submitted info of skill with the given ID
    - Returns success value and new skill basic info
    - Admin rights required

- Input sample:
```bash
{
    "name": "Resourcefulness"
}
```

- Output sample: 

```bash
{
  "skill": {
    "description": "Ability to deal with complex situations and come up with a solution",
    "id": 50,
    "name": "Resourcefulness"
  },
  "success": true
}
```

### DELETE /skills/{skill_id}
- General:
    - Deletes skill with the given ID
    - Returns success value and deleted skill basic info
    - Admin rights required

- Output sample: 

```bash
{
  "skill": {
    "description": "Ability to deal with complex situations and come up with a solution",
    "id": 50,
    "name": "Resourcefulness"
  },
  "success": true
}
```

### GET /endorsements
- General:
    - Returns a list of endorsements, including giver and receiver names, success value and number of endorsements
    - User rights required

- Output sample: 

```bash
{
  "endorsements": [
    {
      "creation_date": "Fri, 15 May 2020 00:00:00 GMT",
      "giver_first_name": "Vincent",
      "giver_id": 106,
      "giver_last_name": "Vega",
      "name": "Problem solving",
      "receiver_first_name": "Vincent",
      "receiver_id": 106,
      "receiver_last_name": "Vega"
    }
  ],
  "num_endorsements": 1,
  "success": true
}
```

### DELETE /endorsements
- General:
    - Deletes all endorsements in the database
    - Returns success value and number of endorsements deleted
    - Admin rights required

- Output sample: 

```bash
{
  "num_endorsements_deleted": 1,
  "success": true
}
```

### POST /endorsements
- General:
    - Creates a new endorsement using the submitted endorsement profile in JSON format. Field name is required
    - Returns success value and new endorsement basic info
    - Admin rights required

- Input sample:
```bash
{
    "giver_id": 106,
    "receiver_id": 106,
    "skill_id": 51
}
```

- Output sample: 

```bash
{
  "endorsement": {
    "creation_date": "Fri, 15 May 2020 00:00:00 GMT",
    "giver_id": 106,
    "id": 37,
    "receiver_id": 106,
    "skill_id": 51
  },
  "success": true
}
```

### DELETE /endorsements/{endorsement_id}
- General:
    - Deletes endorsement with the given ID
    - Returns success value and deleted endorsement basic info
    - Admin rights required

- Output sample: 

```bash
{
  "endorsement": {
    "creation_date": "Fri, 15 May 2020 00:00:00 GMT",
    "giver_id": 106,
    "id": 37,
    "receiver_id": 106,
    "skill_id": 51
  },
  "success": true
}
```

## Testing

There are 2 different ways offered to test the API:

### Postman

[Postman](https://www.postman.com/) is a useful open-source tool for API development and testing. You can download it, import and run the [Postman collection](/endorsa_api_testing.postman_collection.json) which makes different API calls and result checks. You can connect it to your local server or to the Heroku app.

The steps to use Postman are the following:

- Download, install and open [Postman](https://www.postman.com/)
- Import the postman collection `./endorsa_api_testing.postman_collection.json`
- Right click the `endorsa_api_testing` collection folder and modify the `base_url` variable to either the local URL or the Heroku app URL, depending on which one you want to test
- Right-click the collection folder for `admin rights`, `user rights` and `delete_new`, navigate to the authorization tab, and update the JWT in the token field
- Run the collection and check if there are any errors

### Unittest

The file [test_app.py](/test_app.py) allows to test API **running locally** in an easy way. You just have to run it while your API is running in your localhost, using the command:
```bash
python test_app.py
```