# Trivia API

Trivia is a Questions and Answers application

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

### Prerequisites

You need the following applications to run the server app:
1. Python 3.7
2. Pipenv (_Optional_)

You need the following applications to run the client app:
1. Node 11+
2. NPM

### Installing

It is preferred if you run this in a virtual environment for python. If you are using `pipenv`, virtual environment
would be taken care of by `pipenv`. Instructions for setting up a virtual environment for your platform can be found in
the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Installing the server dependencies:
1. Change directory to `./backend`.
2. Install the requirements:
```bash
pipenv install
```
or if you are not using `pipenv`:
```bash
pip install requirements.txt
```

Installing the client dependencies:
1. Change directory to `./frontend`.
2. Install the requirements:
```bash
npm i
```

## Testing

To run the flask tests, run the following command:
```bash
python -m unittest backend.test.test_flaskr.TriviaTestCase
```

## Running the application

Starting the server:
1. Change directory to `./backend`.
2. Run the following commands:
```bash
export FLASK_APP=flaskr
flask run
```
3. The backend application will be serve on **http://localhost:5000**

Starting the client:
1. Change directory to `./frontend`.
2. Run the following script:
```bash
npm run start
```
3. The frontend application will be serve on **http://localhost:3000**

Now, go to **http://localhost:3000** to view the Trivia app.


## API Documentation
* GET "/categories"
    - Request Parameters: None
    - Response Body:
    
    `categories`: Dictionary of *Category ID* <-> *Category Type*
```json
{
  "categories": {
    "1": "Science",
    "2": "Art"
  } 
}
```

* GET "/questions?page=1"
    - Request Parameters: `page`: Page number
    - Response Body:

    `questions`: List of questions

    `categories`: Dictionary of *Category ID* <-> *Category Type*

    `total_questions`: Total number of  questions
```json
{
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }],
  "categories": {
    "1": "Science",
    "2": "Art"
  },
  "total_questions": 1
}
```

* DELETE "/questions/<int:question_id>"
    - Request Parameters: `question_id`: Question ID to delete
    - Response Body:

    `deleted`: Question ID that is deleted
```json
{
  "deleted": 20
}
```

* POST "/questions"
    - Request Body:
    
    `question`: Question statement
    
    `answer`: Answer statement
    
    `category`: Category ID
    
    `difficulty`: Difficulty Level
    - Response Body:
    
    `question`: Question object that is created
```json
{
  "question": {
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }
}
```

* POST "/search"
    - Request Body:
    
    `searchTerm`: Search term
    - Response Body:
    
    `questions`: List of questions found in search
    
    `total_questions`: Total number of  questions
```json
{
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }],
  "total_questions": 1
}
```

* GET "/categories/<int:category_id>/questions"
    - Request Parameters: `category_id`: Category ID for questions
    - Response Body:

    `questions`: List of category questions

    `total_questions`: Total number of  questions
    
    `current_category`: Current category ID
```json
{
  "questions": [{
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }],
  "total_questions": 1,
  "current_category": 1
}
```

* POST "/quizzes"
    - Request Body:
    
    `previous_questions`: List of previously answered questions

    `quiz_category`: Category object of the quiz
    - Response Body:
    
    `question`: Random question of requested category
```json
{
  "question": {
    "id": 1,
    "question": "",
    "answer": "",
    "category": 1,
    "difficulty": 1
  }
}
```
