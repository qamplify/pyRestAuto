from rest_lib import pyRest_lib
import json
import unittest
obj = pyRest_lib.PyRestLib()
auth_id ='MAZJJMYZU5ODA2YZNKYZ'


class Verification(unittest.TestCase):
    sauth_id = ''

    def test_1_create_account(self):
        global sauth_id
        post_data = {'name':'user1','enabled':'True'}
        code,data,headers = obj.send_request\
            ('/Account/MAZJJMYZU5ODA2YZNKYZ/Subaccount/',
             method_name='POST',parameters=post_data)
        print(data)
        self.sauth_id  = data['auth_id']
        print(self.sauth_id)
        self.assertEqual(data['message'],'created')


    def test_2_get_account(self):
        print(self.sauth_id)
        code,data,headers = obj.send_request('/Account/MAZJJMYZU5ODA2YZNKYZ/Subaccount/'+self.sauth_id+'/',method_name='GET')
        print(data)
        data1 = data['objects']
        data2 = data1[0]
        print(data2)
        self.assertEqual(data2['name'],'user1')

