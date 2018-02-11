from rest_lib import pyRest_lib
from common_lib import logger
import unittest



class TestExample(unittest.TestCase):
    rest_obj = pyRest_lib.PyRestLib(url='https://httpbin.org')

    def test_get(self):
        response = self.rest_obj.send_request('/get',method_name='GET')
        code = response['code']
        self.assertEqual(code,200)


    def test_post(self):
        response = self.rest_obj.send_request('/post',method_name='POST',
                                          parameters={'test':'post'})
        code = response['code']
        self.assertEqual(code, 200)

    def test_put(self):
        response = self.rest_obj.send_request('/put',method_name='PUT')
        code = response['code']
        self.assertEqual(code, 200)

    def test_delete(self):
        response = self.rest_obj.send_request('/delete',method_name='DELETE')
        code = response['code']
        self.assertEqual(code, 200)

    def test_upload_file(self):
        data = self.rest_obj.send_request('/post',method_name='POST',
                                          file_path='__file__')

