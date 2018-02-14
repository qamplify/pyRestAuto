import requests
import traceback
from common_lib import parse_yaml, json_parser, logger
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from pathlib import Path


class PyRestLib(object):
    response_timeout = None
    conf_obj = parse_yaml.Yamlparser()
    json_obj = json_parser.JsonParser()
    log_obj = logger.Rest_Logger()
    log = log_obj.get_logger('restLib')
    yaml_data = conf_obj.get_data()

    def __init__(self,url=None):
        # self.log.info('************* Test started ************')
        if url:
            self.url = url
        else:
            self.url = self.yaml_data['url']
        self.auth = self.yaml_data['auth']
        self.auth_type = self.yaml_data['auth_type']
        self.username = self.yaml_data['auth_details']['username']
        self.password = self.yaml_data['auth_details']['password']

    def send_request(self, path, parameters=None, method_name=None,
                     file_path=None):
        """
        :param path: url path
        :param parameters: Request parameters
        :param method_name: method name (GET,POST,PUT,DELETE)
        :param file_path: upload file paths

        :return: This function returns response details
        """

        try:
            if method_name == 'GET':
                response = self.__get_request(path, parameters=parameters)
                return response
            elif method_name == 'POST':
                response = self.__post_request(path, parameters=parameters,
                                               file_paths=file_path)
                return response
            elif method_name == 'PUT':
                response = self.__update_request(path, parameters=parameters)
                return response
            elif method_name == 'DELETE':
                response = self.__delete_request(path)
                return response
            else:
                return 'Method name should be GET/POST/PUT/DELETE. eg:' \
                       ' method_name = "GET"'

        except Exception as e:
            self.log.exception('Got exception in sendrequest method '
                               '{}'.format(e))

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
            self.log.info('************* GET request URL is {} ************'
                          '*'.format(url_path))
            # Checking authentication flog.
            if self.auth is True:
                self.headers = self.yaml_data["headers"]
                if self.auth_type == 'HTTPDigestAuth':
                    self.log.info('Authentication type is HTTPDigestAuth')
                    res = requests.get(url_path, params=parameters,
                                       headers=self.headers,
                                       auth=HTTPDigestAuth(self.username,
                                                           self.password))
                elif self.auth_type == 'HTTPBasicAuth':
                    self.log.info('Authentication type is HTTPBasicAuth')
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
            self.log.info(
                'Received response code is {}'.format(res_status_code))
            self.log.info('Received response data is {}'.format(res_data))
            self.log.debug(
                'Received response headers is {}'.format(res_headers))
            self.log.info('*************----END----*************')
            response['code'] = res_status_code
            # rest_data = self.json_obj.load_json_data(str(res_data))
            response['data'] = res_data
            response['headers'] = res_headers
            # Returning GET request status code, data and headers.
            # return res_status_code, rest_data, res_headers
            return response

        except Exception as e:
            self.log.exception(
                "GET request {} Failed with exception {}".format(url_path, e))

    def __post_request(self, path, parameters=None,file_paths=None):
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
            # headers = self.headers
            # Adding files to POST parameters
            self.headers = self.yaml_data["headers"]
            if file_paths:
                upload_data = self.__upload_files(parameters,file_paths)
                self.headers ['Content-Type'] = upload_data.content_type
                parameters = upload_data
            self.log.info('Parameters are {}'.format(parameters))
            response = {}
            url_path = self.url + path
            self.log.info('*************  POST request URL is {}  '
                          '*************'.format(url_path))

            # Checking authentication flag to send auth details.
            if self.auth is True:
                if self.auth_type == 'HTTPDigestAuth':
                    res = requests.post(url_path, data=parameters,
                                        headers=self.headers,
                                        auth=HTTPDigestAuth(self.username,
                                                            self.password))
                elif self.auth_type == 'HTTPBasicAuth':
                    # self.json_data = self.json_obj.dump_json_data(parameters)
                    res = requests.post(url_path, data=parameters,
                                        headers=self.headers,
                                        auth=HTTPBasicAuth(self.username,
                                                           self.password))
                else:
                    res = requests.post(url_path, data=parameters,
                                        headers=self.headers)
            res_status_code = res.status_code
            res_data = res.text
            res_headers = res.headers
            self.log.info(
                'Received response code is {}'.format(res_status_code))
            self.log.info('Received response data is {}'.format(res_data))
            self.log.debug(
                'Received response headers is {}'.format(res_headers))
            self.log.info('*************----END----*************')
            response['code'] = res_status_code
            # rest_data = self.json_obj.load_json_data(str(res_data))
            response['data'] = res_data
            response['headers'] = res_headers
            # Returning response status code, data and headers
            # return res_status_code, rest_data, res_headers
            return response

        except Exception as e:
            self.log.exception("POST request {} Failed with exception "
                  "{}".format(url_path, e))
            traceback.print_exc()
        except FileNotFoundError as fe:
            self.log.exception("POST request {} Failed with File not found "
                  "{}".format(url_path, fe))


    def __delete_request(self, path):
        try:
            response = {}
            # Framing URL request.
            url_path = self.url + path
            self.log.info('************* DElETE request URL is {}  '
                          '*************'.format(url_path))
            # Checking authentication flog.
            if self.auth is True:
                self.headers = self.yaml_data["headers"]
                if self.auth_type == 'HTTPDigestAuth':
                    res = requests.delete(url_path,
                                          headers=self.headers,
                                          auth=HTTPDigestAuth(self.username,
                                                              self.password))
                elif self.auth_type == 'HTTPBasicAuth':
                    res = requests.delete(url_path,
                                          auth=HTTPBasicAuth(self.username,
                                                             self.password))
            else:
                res = requests.delete(url_path,
                                      headers=self.headers)
            res_status_code = res.status_code
            res_data = res.text
            res_headers = res.headers
            response['code'] = res_status_code
            # if res_data:
            #     rest_data = self.json_obj.load_json_data(str(res_data))
            # else:
            #     rest_data = 'Empty data received'
            response['data'] = res_data
            response['headers'] = res_headers
            self.log.info(
                'Received response code is {}'.format(res_status_code))
            self.log.info('Received response data is {}'.format(res_data))
            self.log.debug(
                'Received response headers is {}'.format(res_headers))
            # Returning GET request status code, data and headers.
            # return res_status_code, rest_data, res_headers
            self.log.info('*************----END----*************')
            return response

        except Exception as e:
            self.log.exception("DELETE request {} Failed with exception "
                  "{}".format(url_path, e))
            traceback.print_exc()

    def __update_request(self, path, parameters=None):
        try:
            response = {}
            url_path = self.url + path
            self.headers = self.yaml_data["headers"]
            self.log.info('*************PUT request URL is {} '
                          '*************'.format(url_path))
            # Checking authentication flag to send auth details.
            if self.auth is True:
                self.headers = self.yaml_data["headers"]
            if self.auth_type == 'HTTPDigestAuth':
                res = requests.put(url_path, data=parameters,
                                   headers=self.headers,
                                   auth=HTTPDigestAuth(self.username,
                                                       self.password))
            elif self.auth_type == 'HTTPBasicAuth':
                self.json_data = self.json_obj.dump_json_data(parameters)
                res = requests.put(url_path, data=self.json_data,
                                   headers=self.headers,
                                   auth=HTTPBasicAuth(self.username,
                                                      self.password))
            else:
                res = requests.put(url_path, data=parameters,
                                   headers=self.headers)
            res_status_code = res.status_code
            res_data = res.text
            res_headers = res.headers
            response['code'] = res_status_code
            # rest_data = self.json_obj.load_json_data(str(res_data))
            response['data'] = res_data
            response['headers'] = res_headers
            # Returning response status code, data and headers
            self.log.info(
                'Received response code is {}'.format(res_status_code))
            self.log.info('Received response data is {}'.format(res_data))
            self.log.debug(
                'Received response headers is {}'.format(res_headers))
            # return res_status_code, rest_data, res_headers
            self.log.info('*************----END----*************')
            return response

        except Exception as e:
            self.log.exception("PUT request {}Failed with exception "
                           "{}".format(url_path, e))
            traceback.print_exc()

    def create_session(self):
        """
        Create a Session and hold that in an instance/object variable.
        :return:
        """
        pass

    def __upload_files(self,params,filenames):
        try:
            self.log.info('Uploading file/s {}'.format(filenames))
            if params is None:
                params = {}
            if filenames:
                for i in range(len(filenames)):
                    file = Path(filenames[i])
                    if file.exists():
                        params['file'+str(i)] = (filenames[i], open(filenames[i],'rb'))
            encoded_data = MultipartEncoder(params)
            upload_data = MultipartEncoderMonitor(encoded_data)
            return upload_data
        except Exception as e:
            self.log.exception(
                "Got Exception when uploading file {}".format(e))

    # This method is not requeired
    def __http_basic_auth(self, user, password):
        """
        creates a
        :param user:
        :param password:
        :return:
        """
        pass
