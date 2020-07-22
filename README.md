# Forum
A place for people with the same interest to share topics, comments, rating

## Deployment
https://forum-dz.herokuapp.com/projects

## Motivation
To create a place for people to share their projects and leave comments on them.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


## API References

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "messages": "detailed error messages"
}
```
The API will return four error types with detailed messages when requests fail:  
 - 400: Bad Request
 - 404: Resource Not Found
 - 422: Not Processable
 - 500: Internal Server Error

### Endpoints
GET '/projects'
- General:
-- Return a list of projects, success value, total number of projects, and its category type.
- Sample: `curl http://127.0.0.1:5000/projects`
```
  {
    "length": 45,
    "projects": [
    {
      "category": 0,
      "datetime": "Wed, 22 Jul 2020 22:06:43 GMT",
      "description": "dummy description",
      "id": 1,
      "image_link": "http://dummy_image_link",
      "labels": "nodejs, momentjs",
      "name": "dummy project1",
      "user_id": 1,
      "video_link": "http://dummy_video_link"
    },
    {
      "category": 1,
      "datetime": "Wed, 22 Jul 2020 22:06:43 GMT",
      "description": "dummy description",
      "id": 2,
      "image_link": "http://dummy_image_link",
      "labels": "nodejs, momentjs",
      "name": "dummy project2",
      "user_id": 2,
      "video_link": "http://dummy_video_link"
    },],
    "success": true
  }
```
GET '/comments/<int:project_id>'
- Fetches a list of comments related to one project_id
- Request Arguments: project_id
- Returns: An object with comments, the project_id, the user_id and datetime when the comments were created. 
- Sample: `curl http://127.0.0.1:5000/comments/4`
```
{
  "comments": [
    {
      "comments": "your project is good 3",
      "datetime": "Wed, 22 Jul 2020 22:06:43 GMT",
      "id": 4,
      "project_id": 4,
      "user_id": 12
    }
  ],
  "length": 1,
  "success": true
}
```
POST '/projects'
- Create a new project
- Request Arguments: JSON input with project name, descriptions, category, labels, video_link and image_link
- Returns: success or not.
- Sample: `curl -X POST http://127.0.0.1:5000/projects -H "Content-Type: application/json" -d '{"name": "test project","description": "I am a project for running tests",
"category": 2,"labels": "nodejs, react, auth0", "image_link": "https://test_image_link", "video_link": "https://test_video_link"}'`
```
  {
    "success":true
  }
```
```
POST '/comments'
- Create a new comment
- Request Arguments: JSON input with comments, project_id and user_id.
- Returns: success or not.
- Sample: `curl -X POST http://127.0.0.1:5000/comments -H "Content-Type: application/json" -d '{"comments": "your project rocks","user_id": 4,"project_id": 6}'`
```
  {
    "success":true
  }
```
PATCH '/projects/<int:project_id>'
- Update a project details in datebase
- Request Arguments: JSON input with project name, descriptions, category, labels, video_link and image_link
- Returns: success or not.
- Sample: `curl -X PATCH http://127.0.0.1:5000/projects/4 -H "Content-Type: application/json" -d '{"name": "test project","description": "I am a project for running tests",
"category": 2,"labels": "nodejs, react, auth0", "image_link": "https://test_image_link", "video_link": "https://test_video_link"}'`
```
  {
    "success":true
  }
```
DELETE '/projects/<int:project_id>'
- Delete a project based on project_id
- Request Arguments: "project_id" in URL
- Returns: If the operation succeeded or not.
- Sample: `curl -X DELETE http://127.0.0.1:5000/projects/28`
```
  {
    "success":true
  }
```

## Deployment N/A
## Authors
Dawei Zhang
## Acknowledgements
The awesome team at Udacity and Coach Caryn.
