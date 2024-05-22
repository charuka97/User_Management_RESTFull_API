# To run this test cace navidate to root directy (\User_Management_RESTFull_API>) of the project
# Run the tests
# python -m unittest discover -s app/tests -p "test_user.py"

# To run all test case inside app/tests fil use bellow command
# python -m unittest discover -s app/tests -p "*.py"

import unittest
import sys
import os

# Append the app directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '...', 'app')))

from app import app

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login(self):
        response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json())
        self.assertIn("refresh_token", response.get_json())

    def test_create_user(self):
        login_response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        access_token = login_response.get_json()["access_token"]

        response = self.app.post(
            "/users/create",
            json={
                "name": "John Doe",
                "email": "charuka@example.com",
                "phone_number": "1234567890",
                "age": 30,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 201)

    def test_user_already_exist_when_create(self):
        login_response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        access_token = login_response.get_json()["access_token"]

        response = self.app.post(
            "/users/create",
            json={
                "name": "John Doe",
                "email": "charuka@example.com",
                "phone_number": "1234567890",
                "age": 30,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 409)

    def test_get_all_users(self):
        login_response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        access_token = login_response.get_json()["access_token"]

        response = self.app.get(
            "/users",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        login_response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        access_token = login_response.get_json()["access_token"]

        user_id = "664d7cc4d8d1217ceb97b145"
        response = self.app.get(
            "/users/get_by_id",
            query_string={"user_id": user_id},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        login_response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        access_token = login_response.get_json()["access_token"]

        email = "john@example.com"
        response = self.app.put(
            "/users/update",
            json={
                "email": email,
                "name": "Updated Name",
                "phone_number": "0987654321",
                "age": 35,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        login_response = self.app.post(
            "/login", json={"email": "charuka@gmail.com", "password": "123jklmB@"}
        )
        access_token = login_response.get_json()["access_token"]

        user_id = "664da3f92637f8dd179c3513"
        response = self.app.delete(
            "/users/delete",
            query_string={"user_id": user_id},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
