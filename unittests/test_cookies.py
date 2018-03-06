# from rest_lib import pyRest_lib
# from common_lib import logger
# import unittest
#
# class Test_cookie(unittest.TestCase):
#     # Creating pyRest_lib object and passing test URL
#     rest_obj = pyRest_lib.PyRestLib(url='https://httpbin.org')
#     # Creating logger object and assigning logger instance
#     log_obj = logger.Rest_Logger()
#     log = log_obj.get_logger('cookie')
#     # Setting session variable True to use cookies
#     rest_obj.session = True
#     def test_verifyCookiefun(self):
#         response = self.rest_obj.send_request\
#             ('/cookies/set/sessioncookie/123456789',method_name='GET')
#         self.assertEqual(response['code'],200)
#
