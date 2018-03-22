from rest_lib import pyRest_lib
import unittest,os

class Test_cookie(unittest.TestCase):

    def setUp(self):
        # Getting test data location
        file = os.path.abspath('resources//config.yaml')
        # Creating object for PyRestLib
        self.rest_obj = pyRest_lib.PyRestLib(url='http://httpbin.org/',
                                             file_path=file,auth='Session')
        # Getting logger object
        self.log = self.rest_obj.get_logObj()
        # Getting json object
        self.json = self.rest_obj.get_jsonObj()

    def test_verifyCookiefun(self):
        """
        This
        """
        self.log.info('Testing cookies')
        response = self.rest_obj.send_request\
            ('/cookies/set/sessioncookie/123456789',method_name='GET')
        # Verifying response code
        self.assertEqual(response['code'],200)
        # Verifying response cookie data
        data = response['data']
        self.assertEqual(self.json.get_key_value(data ,'sessioncookie'),
                         '123456789')

    def test_send_cookie(self):
        """
        This test verifying cookies sending as parameters.
        """
        self.log.info('Sending custom cookie')
        response = self.rest_obj.send_request('/cookies',method_name='GET',
                                              cookies={'sample':'test_cookie'})

        data = response['data']
        res_cookie = self.json.get_key_value(data,'sample')
        # Verifying response cookie data
        self.assertEqual(res_cookie,'test_cookie')




