import unittest
import json
import base64

from src.api.handler import app
from src.api.services import user


class TestHandler(unittest.TestCase):

    def setUp(self):
        # To prepare a fresh database instance for each scenario.
        user.delete_table()
        user.create_table()

        self.app = app.test_client()

        self.content_type = 'application/json'
        self.register_data_valid = dict(email='test@mail.com',
                                        password='passwordsecure',
                                        pin='3412')
        self.register_data_invalid = dict(name='John',
                                          lastname='Doe')

        self.change_password_data_valid = dict(
            email='test@mail.com',
            oldPassword='passwordsecure',
            newPassword='12345'
        )

        self.change_password_data_invalid = dict(
            email='test@mail.com',
            oldPassword='invalid_password',
            newPassword='12345'
        )

    def tearDown(self):
        user.delete_table()

    def test_register_user_success_200(self):
        response = self.app.post('/user/register',
                                 data=json.dumps(self.register_data_valid),
                                 content_type=self.content_type)
        self.assertEqual(200, response.status_code)

    def test_register_user_invalid_payload_400(self):
        response = self.app.post('/user/register',
                                 data=json.dumps(self.register_data_invalid),
                                 content_type=self.content_type)
        self.assertEqual(400, response.status_code)

    def test_retrieve_pin(self):
        # Prepare database for the test
        valid_user = self.register_data_valid
        user.register_user(user.encrypt_user(valid_user))

        headers = {"Authorization": "Basic {}".format(
            base64.b64encode(f'{valid_user["email"]}:{valid_user["password"]}'.encode()).decode("utf8")
        )}
        response = self.app.get('/user/retrievePin', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_change_password_success(self):
        # Prepare database for the test
        valid_user = self.register_data_valid
        user.register_user(user.encrypt_user(valid_user))

        response = self.app.put('/user/changePassword',
                                data=json.dumps(self.change_password_data_valid),
                                content_type=self.content_type)
        self.assertEqual(200, response.status_code)

    def test_change_password_fail(self):
        # Prepare database for the test
        valid_user = self.register_data_valid
        user.register_user(user.encrypt_user(valid_user))

        response = self.app.put('/user/changePassword',
                                data=json.dumps(self.change_password_data_invalid),
                                content_type=self.content_type)
        self.assertEqual(400, response.status_code)

    def test_index_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
