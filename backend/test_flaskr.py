import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the meaning of life?',
            'answer': 42,
            'category': 1,
            'difficulty': 99
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(isinstance(data['categories'], list))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/categories/all')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/13')
        print('res --->', res)
        print('data --->', res.data)
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 13).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 13)
        self.assertTrue(data['total_questions'])
        self.assertEqual(
            question, None
        )

    def test_404_for_failed_delete(self):
        res = self.client().delete('/categories/one_hundred')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # def test_422_if_category_does_not_exist(self):
    #     res = self.client().delete('/categories/1000000')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')

    # def test_post_question(self):
    #     res = self.client().post('/questions', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['posted'])
    #     self.assertTrue(len(data['total_questions']))
    #     self.assertEqual(data, not None)

    # def test_422_for_failed_create(self):
    #     res = self.client().post(
    #         '/questions',  json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')

    # def test_get_question_search_with_results(self):
    #     res = self.client().post(
    #         '/question',  json={'search': 'peanut'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(len(data['question']), 1)

    # def test_get_question_search_without_results(self):
    #     res = self.client().post(
    #         '/question',  json={'search': 'jackfruit'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(len(data['question']), 0)

    #  def test_get_question_within_categories(self):
    #     res = self.client().get('/questions/science')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(isinstance(data['questions'], list))

    # def test_404_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get('/questions/engineering')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    #  def test_play_quiz(self):
    #     res = self.client().post('/play')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(len(data['questions']) > 0)

    # def test_400_for_failed_play(self):
    #     res = self.client().post('/play')

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()