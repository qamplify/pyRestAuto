import requests
from common_lib import parse_yaml, json_parser
from requests.auth import HTTPDigestAuth,HTTPBasicAuth

class PyRestLib(object):
    response_timeout = None
    # global auth_type, username, password
    conf_obj = parse_yaml.Yamlparser()
    auth_type = conf_obj.get_data(branch='auth_type')
    username = conf_obj.get_data(branch='username')
    password = conf_obj.get_data(branch='password')


    def __init__(self):
        self.url = self.conf_obj.get_data(branch='url')

    def send_request(self, path, parameters=None, method_name=None, headers=None):
        """
        :param path: url path
        :param parameters: Request parameters
        :param method_name: method name (GET,POST,PUT,DELETE)
        :param headers: To add any custom headers to the request

        :return: This function returns response details in dict.
        """

        try:
            if method_name == 'GET':
                print(self.auth_type == None)
                response = self.__get_request(path,parameters = parameters,headers = headers,auth_type= self.auth_type,username=self.username,password=self.password)
                return response
            elif method_name == 'POST':
                response = self.__post_request(path, parameters=parameters, headers=headers)
                return response
            elif method_name == 'PUT':
                response = self.__update_request(path, parameters=parameters, headers=headers)
                return response
            elif method_name == 'DELETE':
                response = self.__delete_request(path, parameters=parameters, headers=headers)
                return response
            else:
                return  'Method name should be GET/POST/PUT/DELETE. eg: method_name = "GET"'

        except Exception as e:
            print(e)

    def __get_request(self,path,parameters=None,headers=None,auth_type=None,username=None,password=None):
        """
        :param url:
        :param headers:
        :return:
        """
        # 1. Check Url build properly
        # 2. If there are specific headers , make sure we sending with specific
        # headers
        # 3. Once We get Response
        # 4. Read Response code in to a variable
        # 5. Read Http headers in to a variable (Data type TBD)
        # 6. Read Json data in to a variable
        self.auth_type = auth_type
        try:
            response = {}
            url_path = self.url+path
            print(parameters,headers)
            if self.auth_type == 'HTTPDigestAuth':
                res = requests.get(url_path,parameters=parameters,headers=headers, auth=HTTPDigestAuth(self.username,self.password))
            elif self.auth_type == 'HTTPBasicAuth':
                res = requests.get(url_path,parameters=parameters,headers=headers, auth=HTTPBasicAuth(self.username,self.password))
            else:
                res = requests.get(url_path, params=parameters, headers=headers)
            res_status_code = res.status_code
            res_data = res.text
            res_headers = res.headers
            response['status_code'] = res_status_code
            response['response_data'] = res_data
            response['headers'] = res_headers

            return  response

        except Exception as e:
            print (e)

    def __post_request(self, url, json_data, headers=None):
        """
        Posts the request to defined url.
        :param url:
        :param json_data:
        :param headers:
        :return:
        """
        # 1. Check Url build properly
        # 2. validate json_data is valid
        # 3. If there are specific headers , make sure we sending with specific
        # headers
        # 4. Once We get Response
        # 5. Read Response code in to a variable (Data type TBD)
        # 6. Read Http headers in to another variable

        return

    def __delete_request(self):
        return

    def __update_request(self):
        return

    def create_session(self):
        """
        Create a Session and hold that in an instance/object variable.
        :return:
        """
        pass

    def __http_basic_auth(self, user, password):
        """
        creates a
        :param user:
        :param password:
        :return:
        """
        pass
