'''WeConnect Business Test File'''
import unittest
import json
from V1 import app


class RideTestCase(unittest.TestCase):
    '''Ride Class Tests'''

    def setUp(self):
        self.app = app.test_client(self)
        # User 1
        self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(dict(
                email="daniel@live.com", username="daniel",
                password="12345678")),
            content_type="application/json")

        self.login_user = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(dict(
                username="daniel",
                password="12345678")),
            content_type="application/json")

        self.access_token = json.loads(
            self.login_user.data.decode())['access_token']

        # User 2
        self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(dict(
                email="ken@live.com", username="ken",
                password="12345678")),
            content_type="application/json")

        self.login_user2 = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(dict(
                username="ken", password="12345678")),
            content_type="application/json")

        self.access_token2 = json.loads(
            self.login_user2.data.decode())['access_token']

        # Ride 1
        self.app.post(
            "/api/v1/rides",
            data=json.dumps(dict(
                category="SUV", pick_up="Karen",
                drop_off="CBD", date_time="19th June 11.00 A.M",
                price="Ksh.800")),
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})

        self.dict = dict(
            category="limousine", pick_up="Uthiru",
            drop_off="Nairobi",
            date_time="20th June 12.00 A.M", price="Ksh. 900")                  

    def test_add_ride(self):
        '''Test ride creation'''
        response = self.app.post(
            "/api/v1/rides",
            data=json.dumps(self.dict),
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Ride Successfully Created")

    def test_if_no_token_passed(self):
        '''Test ride creation without auth token'''
        response = self.app.post("/api/v1/rides",
                                 data=json.dumps(self.dict),
                                 headers={
                                     "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 401)

    def test_category_empty(self):
        '''Test for blank category'''
        response = self.app.post(
            "/api/v1/rides",
            data=json.dumps(dict(
                category="", pick_up="UpperHill",
                drop_off="TRM", date_time="21st June 15.00",
                price="Ksh. 500")),
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(
            response_msg['category-Error:']["message"],
            "category cannot be an empty string")

    def test_pick_up_empty(self):
        '''Test for blank pick_up location'''
        response = self.app.post(
            "/api/v1/rides",
            data=json.dumps(dict(
                category="SUV", pick_up="",
                drop_off="CBD", date_time="19th June 11.00 A.M",
                price="Ksh. 800")),
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(
            response_msg['pick_up-Error:']["message"],
            "pick_up cannot be an empty string")

    def test_drop_off_empty(self):
        '''Test for blank drop_off location'''
        response = self.app.post(
            "/api/v1/rides",
            data=json.dumps(dict(
                category="limousine", pick_up="CBD",
                drop_off="", date_time="20th June 10.00 a.m",
                price="Ksh. 700")),
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))

        self.assertEqual(
            response_msg['drop_off-Error:']["message"],
            "drop_off cannot be an empty string")

    def test_get_rides(self):
        '''test get all rides'''
        response = self.app.get(
            "/api/v1/rides",
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)

    def test_get_ride(self):
        '''test get a ride'''
        response = self.app.get(
            "/api/v1/rides/1",
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
                "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)

