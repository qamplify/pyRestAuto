from rest_lib import pyRest_lib
import unittest,os


class Test_RestAPIs(unittest.TestCase):
    """
    REST API unittests with out authentication.
    """

    def setUp(self):
        # Step 1: Creating object for pyRest_lib, passing url
        self.rest = pyRest_lib.PyRestLib(url='https://httpbin.org')
        # Step 2: Getting logger object
        self.log = self.rest.get_logObj()
        # Step 3: Getting json object for converting JSON data to python
        #  readable data and viceversa
        self.json = self.rest.get_jsonObj()

    def test_get_request(self):
        response =  self.rest.send_request('/get',method_name='GET')
        code = response['code']
        self.assertEqual(code,200)

    def test_post_request(self):
        data = {'test':'post'}
        # Converting python dict to JSON data
        json_data = self.json.dump_json_data(data)
        response = self.rest.send_request('/post',method_name='POST',
                                          parameters=json_data)
        code = response['code']
        self.assertEqual(code, 200)

    def test_put_request(self):
        response = self.rest.send_request('/put',method_name='PUT')
        code = response['code']
        self.assertEqual(code, 200)

    def test_delete_request(self):
        response = self.rest.send_request('/delete',method_name='DELETE')
        code = response['code']
        self.assertEqual(code, 200)