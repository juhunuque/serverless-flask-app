import unittest

from src.api.services import user
from src.api.utils.crypt import decrypt_value, encrypt_value


class TestUser(unittest.TestCase):
    def setUp(self):
        # To prepare a fresh database instance for each scenario.
        user.delete_table()
        user.create_table()

        self.valid_user_payload = {
            'email': 'test@mail.com',
            'password': '12345',
            'pin': '1234'
        }
        self.invalid_user_payload = {
            'name': 'John',
            'lastname': 'Doe',
        }

    def tearDown(self):
        user.delete_table()

    def test_validate_register_payload_success(self):
        result = user.validate_register_payload(self.valid_user_payload)
        self.assertTrue(result)

    def test_validate_register_payload_fail(self):
        result = user.validate_register_payload(self.invalid_user_payload)
        self.assertFalse(result)

    def test_encrypt_user_success(self):
        result = user.encrypt_user(self.valid_user_payload)
        self.assertEqual(self.valid_user_payload['password'], decrypt_value(result['password']))
        self.assertEqual(self.valid_user_payload['pin'], decrypt_value(result['pin']))

    def test_register_user_success(self):
        result = user.register_user(self.valid_user_payload)
        self.assertTrue(result)

    def test_get_user_by_email_success(self):
        # Add a value for testing purposes
        user.register_user(self.valid_user_payload)

        result = user.get_user_by_email(self.valid_user_payload['email'])
        self.assertGreaterEqual(1, result['Count'])

    def test_get_user_by_email_fail(self):
        result = user.get_user_by_email(self.valid_user_payload['email'])
        self.assertEqual(0, result['Count'])

    def test_verify_password_success(self):
        password = self.valid_user_payload['password']
        password_encrypted = encrypt_value(password)
        result = user.verify_password(password_encrypted, password)
        self.assertTrue(result)

    def test_verify_password_fail(self):
        password_invalid = 'invalid_password'
        password_encrypted = encrypt_value(self.valid_user_payload['password'])
        result = user.verify_password(password_encrypted, password_invalid)
        self.assertFalse(result)

    def test_decrypt_card_pin_success(self):
        pin = self.valid_user_payload['pin']
        pin_encrypted = encrypt_value(pin)

        result = user.decrypt_card_pin(pin_encrypted)
        self.assertEqual(pin, result)

    def test_decrypt_card_pin_fail(self):
        pin_invalid = 'invalid_pin'
        pin_encrypted = encrypt_value(self.valid_user_payload['pin'])

        result = user.decrypt_card_pin(pin_encrypted)
        self.assertNotEqual(pin_invalid, result)

    def test_encrypt_password_success(self):
        result = user.encrypt_password(self.valid_user_payload['password'])
        self.assertEqual('MTIzNDU=', result)

    def test_encrypt_password_fail(self):
        result = user.encrypt_password(self.valid_user_payload['password'])
        self.assertNotEqual('invalid_password', result)

    def test_change_password_success(self):
        result = user.change_password(self.valid_user_payload)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
