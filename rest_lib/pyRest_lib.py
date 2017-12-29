import requests



class PyRestLib(object):

    def __init__(self):
        pass

    def get_request(self, url, headers=None):
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

        pass

    def post_request(self, url, json_data, headers=None):
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

        pass

    def delete_request(self):
        pass

    def update_request(self):
        pass

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
