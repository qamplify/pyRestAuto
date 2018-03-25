import requests, os
import traceback
from common_lib import json_parser, logger, parse_yaml
from requests.auth import HTTPDigestAuth, HTTPBasicAuth
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from requests_toolbelt import exceptions
from requests_toolbelt.downloadutils import stream
import sys
import random


class PyRestLib(object):
    response_timeout = None
    # conf_obj = parse_test.testparser()
    json_obj = json_parser.JsonParser()
    log_obj = logger.Rest_Logger()
    log = log_obj.get_logger('restLib')
    # test_data = conf_obj.get_data()
    session = False

    def __init__(self, url=None, file_path=None, auth=None):
        # self.log.info('************* Test started ************')

        self.test_data = self.__check_file(file_path)

        if url:
            self.url = url
        else:
            self.url = self.test_data['url']
        if auth:
            self.Auth_type = auth
        else:
            self.Auth_type = self.test_data['Authentication_Type']
        if (self.Auth_type == 'HTTPBasicAuth'
                or self.Auth_type == 'HTTPDigestAuth'):
            self.auth_type = self.Auth_type
            self.username = self.test_data[self.auth_type]['username']
            self.password = self.test_data[self.auth_type]['password']
        elif self.Auth_type == 'Session':
            self.session = True
            self.auth_type = None
            self.req_session = self.__create_session(self.test_data)
        elif self.Auth_type == 'JWT':
            self.auth_type = self.Auth_type
        else:
            self.auth_type = None


    def download_data(self, path, filename=None, dir=None):
        """
        :param path: REST URL API path
        :param filename: file name
        :param dir: File download directory

        :return None
        """
        try:
        # RESTAPI url path
            self.path = path
        # Storing GET request response to variable `res`
            res = self.__get_request(self.path)
            if filename is None:
                filename = 'File_'+str(random.randrange(1,100))
        # Saving file to location
            if dir:
                file = os.path.join(dir, filename)
        # Creating downloads folder to project and saving file
            else:
                self.dir = os.path.join(self.cw, 'downloads')
                if os.path.exists(self.dir):
                    os.makedirs(self.dir)
                file = os.path.join(self.dir, filename)
        # Saving response data to file
            with open(file, 'wb') as d_file:
                filename = stream.stream_response_to_file(res, path=d_file)
                self.log.info('File'
                              ' Downloaded to location {}'.format(filename))
        except Exception as e:
            self.log.exception('Got exception file download the file'
                               ' {}'.format(e))



    def upload_data(self, path, **args):
        """ Send request with single or multiple file uploads

        :param path: URL request path
        :param \*\*args: arguments for POST parameters and file names
        :rtype: response
        """

        try:
            if 'file_path' in args:
                file_paths = args['file_path']
            else:
                file_paths = None
            if 'parameters' in args:
                param = args['parameters']
            else:
                param = None
            response = self.__post_request(path, parameters=param,
                                           file_paths=file_paths)
            return response
        except Exception as e:
            self.log.exception('Got exception in upload request {}'.format(e))

    def send_request(self, path, parameters=None, method_name=None,**kwargs):
        """
        :param path: url path
        :param parameters: Request parameters
        :param method_name: method name (GET,POST,PUT,DELETE)
        :param file_path: upload file paths

        :return: This function returns response details
        """

        try:
            if method_name == 'GET':
                response = self.__get_request(path, parameters=parameters,**kwargs)
                return response
            elif method_name == 'POST':
                response = self.__post_request(path, parameters=parameters,**kwargs)
                return response
            elif method_name == 'PUT':
                response = self.__update_request(path, parameters=parameters,**kwargs)
                return response
            elif method_name == 'DELETE':
                response = self.__delete_request(path,**kwargs)
                return response
            else:
                return 'Method name should be GET/POST/PUT/DELETE. eg:' \
                       ' method_name = "GET"'

        except Exception as e:
            self.log.exception('Got exception in sendrequest method '
                               '{}'.format(e))

    def __get_request(self, path, parameters=None, **args):
        """ Sending GET request.
        :param path: path for get request api
        :param headers: headers parameter for adding custom headers
        :return: This method return get request response
        """
        try:
            if self.session:
                req = self.req_session
                test_cookies = args.get('cookies',None)
            else:
                req = requests
            response = {}
            # Framing URL request.
            url_path = self.url + path
            self.log.info('************* GET request URL is {} ************'
                          '*'.format(url_path))
            # Checking authentication flog.
            self.headers = self.test_data["headers"]
            print(self.auth_type)
            if self.auth_type == 'HTTPDigestAuth':
                self.log.info('Authentication type is HTTPDigestAuth')
                res = req.get(url_path, params=parameters,
                              headers=self.headers,
                              auth=HTTPDigestAuth(self.username,
                                                  self.password))
            elif self.auth_type == 'HTTPBasicAuth':
                self.log.info('Authentication type is HTTPBasicAuth')
                res = req.get(url_path, params=parameters,
                              headers=self.headers,
                              auth=HTTPBasicAuth(self.username,
                                                 self.password))

            elif test_cookies:
                 res = req.get(url_path, params=parameters,
                                  headers=self.headers,cookies=test_cookies)
            else:
                res = req.get(url_path, params=parameters,
                              headers=self.headers)
            response['code'] = res.status_code
            response['data'] = res.text
            response['headers'] = res.headers
            self.log.info(
                'Received response code is {}'.format(res.status_code))
            self.log.info('Received response data is {}'.format(res.text))
            self.log.debug(
                'Received response headers is {}'.format(res.headers))
            self.log.info('*************----END----*************')
            # Returning GET request status code, data and headers.
            # return res_status_code, rest_data, res_headers
            return response

        except Exception as e:
            self.log.exception(
                "GET request {} Failed with exception {}".format(url_path, e))

    def __post_request(self, path, parameters=None, file_paths=None,**kwargs):
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
            if self.session:
                req = self.req_session
            else:
                req = requests
            # headers = self.headers
            # Adding files to POST parameters
            self.headers = self.test_data["headers"]
            if file_paths:
                upload_data = self.__upload_files(parameters, file_paths)
                self.headers['Content-Type'] = upload_data.content_type
                parameters = upload_data
            self.log.info('Parameters are {}'.format(parameters))
            response = {}
            url_path = self.url + path
            self.log.info('*************  POST request URL is {}  '
                          '*************'.format(url_path))

            # Checking authentication flag to send auth details.
            if self.auth_type == 'HTTPDigestAuth':
                res = req.post(url_path, data=parameters,
                               headers=self.headers,
                               auth=HTTPDigestAuth(self.username,
                                                   self.password))
            elif self.auth_type == 'HTTPBasicAuth':
                # self.json_data = self.json_obj.dump_json_data(parameters)
                res = req.post(url_path, data=parameters,
                               headers=self.headers,
                               auth=HTTPBasicAuth(self.username,
                                                  self.password))
            else:
                res = req.post(url_path, data=parameters,
                               headers=self.headers)
            self.log.info(
                'Received response code is {}'.format(res.status_code))
            self.log.info('Received response data is {}'.format(res.text))
            self.log.debug(
                'Received response headers is {}'.format(res.headers))
            self.log.info('*************----END----*************')
            response['code'] = res.status_code
            # rest_data = self.json_obj.load_json_data(str(res_data))
            response['data'] = res.text
            response['headers'] = res.headers
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
            if self.session:
                req = self.req_session
            else:
                req = requests
            response = {}
            # Framing URL request.
            url_path = self.url + path
            self.log.info('************* DElETE request URL is {}  '
                          '*************'.format(url_path))
            # Checking authentication flog.
            self.headers = self.test_data["headers"]
            if self.auth_type == 'HTTPDigestAuth':
                res = req.delete(url_path,
                                 headers=self.headers,
                                 auth=HTTPDigestAuth(self.username,
                                                     self.password))
            elif self.auth_type == 'HTTPBasicAuth':
                res = req.delete(url_path,
                                 auth=HTTPBasicAuth(self.username,
                                                    self.password))
            else:
                res = req.delete(url_path,
                                 headers=self.headers)
            response['code'] = res.status_code
            response['data'] = res.text
            response['headers'] = res.headers
            self.log.info(
                'Received response code is {}'.format(res.status_code))
            self.log.info('Received response data is {}'.format(res.text))
            self.log.debug(
                'Received response headers is {}'.format(res.headers))
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
            if self.session:
                req = self.req_session
            else:
                req = requests
            response = {}
            url_path = self.url + path
            self.headers = self.test_data["headers"]
            self.log.info('*************PUT request URL is {} '
                          '*************'.format(url_path))
            # Checking authentication flag to send auth details.
            self.headers = self.test_data["headers"]
            if self.auth_type == 'HTTPDigestAuth':
                res = req.put(url_path, data=parameters,
                              headers=self.headers,
                              auth=HTTPDigestAuth(self.username,
                                                  self.password))
            elif self.auth_type == 'HTTPBasicAuth':
                self.json_data = self.json_obj.dump_json_data(parameters)
                res = req.put(url_path, data=self.json_data,
                              headers=self.headers,
                              auth=HTTPBasicAuth(self.username,
                                                 self.password))
            else:
                res = req.put(url_path, data=parameters,
                              headers=self.headers)
            response['code'] = res.status_code
            # rest_data = self.json_obj.load_json_data(str(res_data))
            response['data'] = res.text
            response['headers'] = res.headers
            # Returning response status code, data and headers
            self.log.info(
                'Received response code is {}'.format(res.status_code))
            self.log.info('Received response data is {}'.format(res.text))
            self.log.debug(
                'Received response headers is {}'.format(res.headers))
            # return res_status_code, rest_data, res_headers
            self.log.info('*************----END----*************')
            return response

        except Exception as e:
            self.log.exception("PUT request {}Failed with exception "
                               "{}".format(url_path, e))
            traceback.print_exc()

    def __create_session(self,data):
        """
        Create a Session and hold that in an instance/object variable.
        :return: request cookie object
        """

        try:
            test_data = data
            # Getting session parameter from config.test file
            sess = requests.Session()
            # Getting authentication & cookie header details from config
            cookie_headers = self.test_data['Session']['cookie_header']
            Authenticatin = self.test_data['Session']['Auth']
            if Authenticatin is True:
                auth_user = self.test_data['Session']['username']
                auth_pass = self.test_data['Session']['password']
                # Adding session authentication details
                sess.auth = (auth_user, auth_pass)
            if cookie_headers:
                # Updating headers with cookie headers
                sess.headers.update(cookie_headers)
            return sess
        except Exception as e:
            self.log.exception('Got exception in session obj creation'
                               '{}'.format(e))

    def __upload_files(self, params, filenames):
        try:
            self.log.info('Uploading file/s {}'.format(filenames))
            if params is None:
                params = {}
            if filenames:
                for i in range(len(filenames)):
                    file = os.path.abspath(filenames[i])
                    if file.exists():
                        params['file' + str(i)] = (filenames[i],
                                                   open(filenames[i], 'rb'))
            encoded_data = MultipartEncoder(params)
            upload_data = MultipartEncoderMonitor(encoded_data)
            return upload_data
        except Exception as e:
            self.log.exception(
                "Got Exception when uploading file {}".format(e))

    # This method is not required. Deprecated
    def __http_basic_auth(self, user, password):
        """
        creates a
        :param user:
        :param password:
        :return:
        """
        pass

    def get_logObj(self):
        # returns logger object
        return self.log

    def get_jsonObj(self):
        # return json object
        return self.json_obj

    def get_confObj(self):
        # return test config object
        return self.conf_obj

    def __check_file(self, file):
        try:
            obj = parse_yaml.Yamlparser(filename=file)
            data = obj.get_data()
            return data
        except Exception as e:
            self.log.exception('Got error in yaml file {}'.format(e))
            sys.exit(1)