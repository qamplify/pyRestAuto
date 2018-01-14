import requests
import traceback
from common_lib import parse_yaml, json_parser
from requests.auth import HTTPDigestAuth, HTTPBasicAuth


class PyRestLib(object):
    response_timeout = None
    conf_obj = parse_yaml.Yamlparser()
    json_obj = json_parser.JsonParser()

    def __init__(self):
        self.url = self.conf_obj.get_data(branch='url')
        self.auth = self.conf_obj.get_data(branch='auth')
        self.auth_type = self.conf_obj.get_data(branch='auth_type')
        self.auth_details = self.conf_obj.get_data(branch='auth_details')

    def send_request(self, path, parameters=None, method_name=None,
                     headers=None):
        """
        :param path: url path
        :param parameters: Request parameters
        :param method_name: method name (GET,POST,PUT,DELETE)

        :return: This function returns response details
        """

        try:
            if method_name == 'GET':
                response = self.__get_request(path, parameters=parameters)
                return response

            elif method_name == 'POST':
                response = self.__post_request(path, parameters=parameters)
                return response
            elif method_name == 'PUT':
                response = self.__update_request(path, parameters=parameters,
                                                 headers=headers)
                return response

            elif method_name == 'DELETE':
                response = self.__delete_request(path, parameters=parameters)
                return response
            else:
                return 'Method name should be GET/POST/PUT/DELETE. eg: method_name = "GET"'

        except Exception as e:
            print(e)

    def __get_request(self, path, parameters=None):
        """ Sending GET request.
        :param path: path for get request api
        :param headers: headers parameter for adding custom headers
        :return: This method return get request response
        """
        # 1. Check Url build properly
        # 2. If there are specific headers , make sure we sending with specific
        # headers
        # 3. Once We get Response
        # 4. Read Response code in to a variable
        # 5. Read Http headers in to a variable (Data type TBD)
        # 6. Read Json data in to a variable

        try:
            response = {}
            # Framing URL request.
            url_path = self.url + path
            # Checking authentication flog.
            if self.auth is True:
                login = self.auth_details.split(',')
                self.username = login[0]
                self.password = login[1]
                self.headers = self.conf_obj.get_data(branch="headers")
                if self.auth_type == 'HTTPDigestAuth':
                    res = requests.get(url_path, params=parameters,
                                   headers=self.headers,
                                   auth=HTTPDigestAuth(self.username,
                                                       self.password))
                elif self.auth_type == 'HTTPBasicAuth':
                    res = requests.get(url_path, params=parameters,
                                   headers=self.headers,
                                   auth=HTTPBasicAuth(self.username,
                                                      self.password))
            else:
                res = requests.get(url_path, params=parameters,
                                   headers=self.headers)
            res_status_code = res.status_code
            res_data = res.text
            res_headers = res.headers
            response['status_code'] = res_status_code
            rest_data = self.json_obj.load_json_data(str(res_data))
            response['response_data'] = rest_data
            response['headers'] = res_headers
            # Returning GET request status code, data and headers.
            return res_status_code,rest_data,res_headers

        except Exception as e:
            print("GET request {} Failed with exception {}".format(url_path,e))
            traceback.print_exc()

    def __post_request(self, path, parameters=None):
        """
        Posts the request to defined url.
        :param path: path for get request api
        :param headers: headers parameter for adding custom headers
        :return: This method return POST request response
        """
        # 1. Check Url build properly
        # 2. validate json_data is valid
        # 3. If there are specific headers , make sure we sending with specific
        # headers
        # 4. Once We get Response
        # 5. Read Response code in to a variable (Data type TBD)
        # 6. Read Http headers in to another variable
        try:
            response = {}
            url_path = self.url + path
            self.headers = self.conf_obj.get_data(branch="headers")
            # Checking authentication flag to send auth details.
            if self.auth is True:
                # Getting authentication credentials from YAML config file.
                login = self.auth_details.split(',')
                self.username = login[0]
                self.password = login[1]
            if self.auth_type == 'HTTPDigestAuth':
                res = requests.post(url_path, data=parameters,
                                    headers=self.headers,
                                   auth=HTTPDigestAuth(self.username,
                                                       self.password))
            elif self.auth_type == 'HTTPBasicAuth':
                    self.json_data = self.json_obj.dump_json_data(parameters)
                    res = requests.post(url_path, data=self.json_data,
                                   headers=self.headers,
                                   auth=HTTPBasicAuth(self.username,
                                                      self.password))
            else:
                res = requests.post(url_path, data=parameters,
                               headers=self.headers)
            res_status_code = res.status_code
            res_data = res.text
            res_headers = res.headers
            response['status_code'] = res_status_code
            rest_data = self.json_obj.load_json_data(str(res_data))
            response['response_data'] = rest_data
            response['headers'] = res_headers
            # Returning response status code, data and headers
            return res_status_code, rest_data, res_headers

        except Exception as e:
            print("POST request {} Failed with exception {}".format(url_path, e))
            traceback.print_exc()

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