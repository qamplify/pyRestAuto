# import pytest
# from rest_lib import pyRest_lib
# import unittest
# from common_lib import logger
#
# obj = pyRest_lib.PyRestLib()
# # TODO Read from config yaml file
# auth_id = 'MAZJJMYZU5ODA2YZNKYZ'
# sauth = ''
#
#
# class Verification(unittest.TestCase):
#     obj1 = logger.Rest_Logger()
#     log = obj1.get_logger('testing')
#
#     @pytest.mark.skip(reason="no way of currently testing this")
#     def test_1_create_account(self):
#         global sauth_id
#         post_data = {'name': 'user13', 'enabled': 'True'}
#         response = obj.send_request('/Account/MAZJJMYZU5ODA2YZNKYZ/Subaccount/',
#                                       method_name='POST', parameters=post_data)
#         data = response['data']
#         sauth_id = data['auth_id']
#         self.assertEqual(data['message'], 'created')
#
#     @pytest.mark.skip(reason="no way of currently testing this")
#     def test_2_get_account(self):
#         response = obj.send_request('/Account/MAZJJMYZU5ODA2YZNKYZ/'
#                                 'Subaccount/'+sauth_id+'/', method_name='GET')
#         data = response['data']
#         self.assertEqual(data['name'], 'user13')
#
#     @pytest.mark.skip(reason="no way of currently testing this")
#     def test_3_delete_account(self):
#         response = obj.send_request(
#             '/Account/MAZJJMYZU5ODA2YZNKYZ/Subaccount/' + sauth_id + '/',
#             method_name='DELETE')
#         code = response['code']
#         self.assertEqual(code, 204)
