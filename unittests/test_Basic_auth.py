from rest_lib import pyRest_lib
import unittest,os


class Test_BasicAuth(unittest.TestCase):

    def setUp(self):
        # Getting test data location
        file = os.path.abspath('resources//config.yaml')
        # Creating object for PyRestLib
        self.rest_obj = pyRest_lib.PyRestLib(file_path=file)
        # Getting logger object
        self.log = self.rest_obj.get_logObj()
        # Getting json object
        self.json = self.rest_obj.get_jsonObj()

    def test_get_following(self):
        """
        Verifying response code for following GET request.
        """
        path = '/user/following'
        response = self.rest_obj.send_request(path,method_name='GET')
        code = response['code']
        data = response['data']
        self.assertEqual(code,200)

    def test_follow_user(self):
        path = '/user/following/jeevan449'
        response = self.rest_obj.send_request(path,method_name='PUT')
        self.assertEqual(response['code'],204)

    def test_unfollow_user(self):
        path = '/user/following/jeevan449'
        response = self.rest_obj.send_request(path,method_name='DELETE')
        self.assertEqual(response['code'],204)

    def test_get_starred_gists(self):
        path = '/gists/starred'
        response = self.rest_obj.send_request(path,method_name='GET')
        self.assertEqual(response['code'],200)

    def test_post_A_gist(self):
        """
        Posting a GIST data to git hub
        """
        self.log.info('Testing gist upload data...')
        path = '/gists'
        gist_data = {
            "description": "This is sample gist. Testing pyRestAuto",
            "public": True,
            "files": {
                "file.txt": {
                    "content": "Sample data"
                }
            }
        }
        response = self.rest_obj.send_request(path,method_name='POST',
                            parameters=self.json.dump_json_data(gist_data))
        self.assertEqual(response['code'],201)


    def test_start_gist(self):
        path = '/gists/16d4474f9318c6ae1d373070a7f09cc7/star'
        response = self.rest_obj.send_request(path,method_name='PUT')
        self.assertEqual(response['code'],204)

    def test_veriy_gistStarred(self):
        path = '/gists/16d4474f9318c6ae1d373070a7f09cc7/star'
        response = self.rest_obj.send_request(path, method_name='GET')
        self.assertEqual(response['code'], 404)

    def test_unstar_gist(self):
        path = '/gists/16d4474f9318c6ae1d373070a7f09cc7/star'
        response = self.rest_obj.send_request(path,method_name='DELETE')
        self.assertEqual(response['code'],204)

    def test_verify_gistUnStarred(self):
        path = '/gists/16d4474f9318c6ae1d373070a7f09cc7/star'
        response = self.rest_obj.send_request(path, method_name='GET')
        self.assertEqual(response['code'], 404)

