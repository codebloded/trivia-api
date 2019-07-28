import random
import re

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from backend.database.models import setup_db, Category, Question

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    """
    Creates and sets up a Flask application
    :param test_config:
    :return: Flask application
    """
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def set_headers(response):
        """
        Intercept response to add 'Access-Control-Allow' headers
        :param response: HTTP Response
        :return: Modified HTTP Response
        """
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        """
        Creates a dictionary of all categories
        :return: All categories
        """
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        return jsonify({
            'categories': categories
        })

    '''
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        """
        Get all questions, categories and total questions from database
        :return: Questions, categories and total questions
        """
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        questions = [question.format() for question in Question.query.all()]
        page = int(request.args.get('page', '0'))
        upper_limit = page * 10
        lower_limit = upper_limit - 10
        return jsonify({
            'questions': questions[lower_limit:upper_limit] if page else questions,
            'total_questions': len(questions),
            'categories': categories
        })

    '''
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Delete a question using question id
        :param question_id: Id of the question to be deleted
        :return: Id of the question that has been deleted
        """
        if not question_id:
            return abort(400, 'No question id provided')
        question = Question.query.get(question_id)
        if not question:
            return abort(404, f'No question found with id: {question_id}')
        question.delete()
        return jsonify({
            'deleted': question_id
        })

    '''
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def post_question():
        """
        Adds a question to database
        :return: The question that is added
        """
        question = Question(
            question=request.json['question'],
            answer=request.json['answer'],
            difficulty=request.json['difficulty'],
            category=request.json['category']
        )
        question.insert()
        return jsonify({
            'question': question.format()
        })

    '''
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/search', methods=['POST'])
    def search():
        """
        Search for questions using the search term
        :return: Searched questions and total questions
        """
        search_term = request.json['searchTerm']
        questions = [question.format() for question in Question.query.all() if
                     re.search(search_term, question.question, re.IGNORECASE)]
        return jsonify({
            'questions': questions,
            'total_questions': len(questions)
        })

    '''
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        """
        Gets questions from database and filters them based on category
        :param category_id: The category for which questions are to be filtered
        :return: Filtered questions, total questions and current category
        """
        category = Category.query.get(category_id)
        questions = [question.format() for question in Question.query.all() if
                     question.category == category.id]
        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': category_id
        })

    '''
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        """
        Gets question for quiz
        :return: Uniques quiz question or None
        """
        previous_questions = request.json['previous_questions']
        quiz_category = request.json['quiz_category']
        all_questions = Question.query.all()
        questions = [question.format() for question in all_questions if
                     question.category == int(quiz_category['id']) or not quiz_category['id']]
        if len(previous_questions) == len(questions):
            return jsonify({})
        question = random.choice(questions)
        while any(question_id == question['id'] for question_id in previous_questions):
            question = random.choice(questions)
        return jsonify({
            'question': question
        })

    # Error Handler
    @app.errorhandler(HTTPException)
    def http_exception_handler(error):
        """
        HTTP error handler for all endpoints
        :param error: HTTPException containing code and description
        :return: error: HTTP status code, message: Error description
        """
        return jsonify({
            'success': False,
            'error': error.code,
            'message': error.description
        }), error.code

    @app.errorhandler(Exception)
    def exception_handler(error):
        """
        Generic error handler for all endpoints
        :param error: Any exception
        :return: error: HTTP status code, message: Error description
        """
        return jsonify({
            'success': False,
            'error': 500,
            'message': f'Something went wrong: {error}'
        }), 500

    return app
