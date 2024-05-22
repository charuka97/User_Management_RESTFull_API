# To run this test cace navidate to root directy (\User_Management_RESTFull_API\app\tests>) of the project
# then run
# "python -m unittest test_auth"

import unittest
import sys
import os

# Get the current file's directory and append the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '...', 'app')))

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
