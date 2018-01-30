from rest_lib import pyRest_lib
import unittest
from common_lib import logger

obj = pyRest_lib.PyRestLib()
# TODO Read from config yaml file
auth_id = 'MAZJJMYZU5ODA2YZNKYZ'
sauth = ''


class Verification(unittest.TestCase):
    obj = logger.Rest_Logger()
    log = obj.get_logger('UnitTest')

    def test_1_create_account(self):
        global sauth_id
        post_data = {'name': 'user11', 'enabled': 'True'}
        code, data, headers = obj.send_request('/Account/MAZJJMYZU5ODA2YZNKYZ/Subaccount/',
                                               method_name='POST', parameters=post_data)
        self.log.info('This is testing')
        self.log.info(data)
        sauth_id = data['auth_id']
        self.assertEqual(data['message'], 'created')

    def test_2_get_account(self):
        code, data, headers = obj.send_request('/Account/MAZJJMYZU5ODA2YZNKYZ/'
                                               'Subaccount/'+sauth_id+'/', method_name='GET')
        self.assertEqual(data['name'], 'user1')

    def test_3_delete_account(self):
        code, data, headers = obj.send_request(
            '/Account/MAZJJMYZU5ODA2YZNKYZ/Subaccount/' + sauth_id + '/',
            method_name='DELETE')
        self.assertEqual(code, 204)
