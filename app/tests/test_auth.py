# To run this test cace navidate to root directy (\User_Management_RESTFull_API\>) of the project
# Run the tests
# python -m unittest discover -s app/tests -p "test_auth.py"

# To run all test case inside app/tests fil use bellow command
# python -m unittest discover -s app/tests -p "*.py"

import unittest
from app import app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_registration(self):
        response = self.app.post(
            "/register", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        self.app.post(
            "/register", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json())
        self.assertIn("refresh_token", response.get_json())

    def test_logout(self):
        self.app.post(
            "/register", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )

        login_response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        access_token = login_response.get_json()["access_token"]

        response = self.app.post(
            "/logout", headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Successfully logged out")

    def test_refresh(self):

        self.app.post(
            "/register", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )

        login_response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        access_token = login_response.get_json()["access_token"]

        self.assertEqual(login_response.status_code, 200)

        refresh_response = self.app.post(
            "/refresh", headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn("access_token", refresh_response.get_json())


"""
request_password_reset
reset_password

not configure yet
"""
# def test_request_password_reset(self):
#     self.app.post('/register', json={
#         'email': 'charuka@gmail.com',
#         'password': '123jklmB@'
#     })
#     response = self.app.post('/request-password-reset', json={'email': 'charuka@gmail.com'})
#     self.assertEqual(response.status_code, 200)

# def test_reset_password(self):
#     self.app.post('/register', json={
#         'email': 'charuka@gmail.com',
#         'password': '123jklmB@'
#     })
#     response = self.app.post('/request-password-reset', json={'email': 'charuka@gmail.com'})
#     reset_token = "extracted_token_from_email"
#     response = self.app.post('/reset-password', json={
#         'token': reset_token,
#         'new_password': 'new_123jklmB@'
#     })
#     self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
