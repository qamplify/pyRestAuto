from rest_lib import pyRest_lib
from rest_lib import pyrest_jwt_lib
import unittest
class Test_JWT_API(unittest.TestCase):
    jwt_token = ''

    def setUp(self):
        self.rest = pyRest_lib.PyRestLib(url='http://181.215.27.157:5000')
        self.json = self.rest.get_jsonObj()
        self.log = self.rest.get_logObj()

    def test_get_1_token(self):
        global jwt_token1
        params = {"username":"user1","password":"abcxyz"}
        response = self.rest.send_request('/auth',parameters=self.json.dump_json_data(params),method_name='POST')
        data = response['data']
        jwt_token1 = self.json.get_key_value(data,'access_token')
        self.rest.set_token(jwt_token1)
        self.assertEqual(response['code'],200)

    def test_get_2_data(self):
        response = self.rest.send_request('/protected',method_name='GET',headers={"Authorization":"JWT "+jwt_token1})
        data = response['data']
        self.assertEqual(response['code'],200)