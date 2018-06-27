'''Models.py'''
from werkzeug.security import generate_password_hash


class User(object):
    '''Class User'''
    # Class Variables
    user_id = 0
    users = {}

    def __init__(self, email, username, password):
        # Class Constructor
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def create_user(self):
        '''Method to create a user'''
        # Every call to this call updates the users dictionary
        # users dictionary has a key user_id whose
        # value is a dictionay with user attributes
        User.user_id += 1
        self.users.update({
            self.user_id:{
                'email':self.email,
                'username':self.username,
                'password':self.password
                }
        })
        return self.users
    @staticmethod
    def change_password(user_name, data):
        '''Method to reset password'''
        person = User.users
        for key in person:
            if person[key]['username'] == user_name:
                if 'new_password' in data.keys():
                    person[key]['password'] = generate_password_hash(data['new_password'])
                    return person


class Ride(object):
    '''Ride class'''

    # Class Variables
    ride_id = 0
    ride = {}

    def __init__(
        self, category, pick_up,
        drop_off, date_time, price, username
    ):
        '''Initialize'''
        self.category = category
        self.pick_up = pick_up
        self.drop_off = drop_off
        self.date_time = date_time
        self.price = price
        self.username = username

    def create_ride(self):
        '''Create a ride'''
        Ride.ride_id += 1
        self.ride.update({
            self.ride_id: {
                'user_id': User.user_id,
                'category': self.category,
                'pick_up': self.pick_up,
                'drop_off': self.drop_off,
                'date_time': self.date_time,
                'price': self.price,
                'owner': self.username
            }
        })
        return self.ride

    @staticmethod
    def get_all_rides():
        '''method to get all rides'''
        rides = Ride.ride
        if len(rides) > 0:
            return rides
        else:
            return {"message": "No rides.Please add one"}

    @staticmethod
    def delete_ride(ride_id):
        '''method to delete a ride'''
        del_ride = Ride.ride
        for key in del_ride:
            if key == ride_id:
                del del_ride[key]

                return {"message": "Deleted Successfully"}

    @staticmethod
    def get_ride(ride_id):
        '''method to get a ride'''
        my_ride = Ride.ride
        for key in my_ride:
            if key == ride_id:
                return my_ride[key]

    @staticmethod
    def update_ride(ride_id, data):
        '''method to update a ride'''

        njaro = Ride.ride
        for key in njaro:
            if key == ride_id:
                if 'category' in data.keys():
                    njaro[key]['category'] = data['category']
                if 'pick_up' in data.keys():
                    njaro[key]['pick_up'] = data['pick_up']
                if 'drop_off' in data.keys():
                    njaro[key]['drop_off'] = data['drop_off']
                if 'date_time' in data.keys():
                    njaro[key]['date_time'] = data['date_time']
                if 'price' in data.keys():
                    njaro[key]['price'] = data['price']
                return njaro


class Request(Ride):
    '''Class Reviews'''
    # Class variables
    request_id = 0
    requests = {}

    def __init__(self, requester):
        '''initializes'''
        self.requester = requester

    def add_request(self):
        '''add a request'''
        Request.request_id += 1
        self.requests.update({
            self.request_id: {
                'user_id': User.user_id,
                'ride_id': Ride.ride_id,
                'requester': self.requester
            }
        })
        return self.requests


    @staticmethod
    def get_all_requests():
        '''method to get all requests'''
        requests = Request.requests
        if len(requests) > 0:
            return requests
        else:
            return {"message":"No Requests for this Ride.Please request"}

    @staticmethod
    def delete_request(request_id):
        '''method to delete a ride'''
        del_request = Request.request
        for key in del_request:
            if key == request_id:
                del del_request[key]
                return {"message": "Deleted Successfully"}

