'''Test Ride requests'''
import unittest
import json
from V1 import app


class RequestsTestCase(unittest.TestCase):
    '''Reviews Class Tests'''

    def setUp(self):
        self.app = app.test_client(self)
        # User 1 registration
        self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(dict(
                email="katumbasam@live.com", username="katumba",
                password="12345678")), content_type="application/json")
        # User 2 registration
        self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(dict(
                email="kenmigoma@gmail.com", username="migoma",
                password="12345678")), content_type="application/json")

        self.user = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(dict(
                username="katumba",
                password="12345678")), content_type="application/json")
        self.access_token = json.loads(self.user.data.decode())['access_token']

        self.user = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(dict(
                username="migoma",
                password="12345678")), content_type="application/json")

        # Ride 1
        self.app.post(
            "/api/v1/rides",
            data=json.dumps(dict(
                category="SUV", pick_up="Bukoto",
                drop_off="Acacia", date_time="20th June 12.00 A.M",
                price="UGX. 5000")),
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})

        self.dict = dict(
            category="Limousine", pick_up="Bukoto",
            drop_off="Acacia", date_time="20th June 12.00 A.M",
            price="UGX. 5000")

    def test_add_request(self):
        '''test add request'''
        response = self.app.post(
            "/api/v1/rides/1/requests",
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 201)

    def test_get_requests(self):
        '''Test get all requests'''
        response = self.app.get(
            "/api/v1/rides/requests",
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
