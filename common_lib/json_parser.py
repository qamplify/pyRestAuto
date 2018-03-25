import simplejson as json
import traceback
from json_digger.json_digger import JsonDigger as JD
from common_lib import logger

class JsonParser(object):
    logger1 = logger.Rest_Logger()
    log = logger1.get_logger('Json_Lib')

    def __init__(self):
        pass

    def validate_json(data):
        """
        Checks if json is valid or not.
        returns True if valid, else False
        :param data: json data
        :return: True if valid, else False
        """
        try:
            json.dumps(data)
            return True
        except Exception as e:
            return False

    def load_json_data(self, data):
        try:
            return json.loads(data)
        except Exception as e:
            self.log.exception("Got exception when "
                               "load json data {}".format(data))
            traceback.print_exc()

    def dump_json_data(self, data):
        #Returning python data type
        return json.dumps(data)

    def parse(self):
        pass

    def get_key_value(self,data,key):
        try:
            # Checking data type dict or any type
            if type(data) != dict:
                # converting data to `dict` type
                data = self.load_json_data(data)
            search = JD(data)
            # Finding key in the data
            values = search.get_keys(key)
            # if one key found returning its value
            if len(values) == 1:
                for i in values:
                    data = values[i]
                return data[0]
            # If key not found returning key not found string
            elif len(values) < 1:
                return  'Key Not Found'
            # if more than one key found returning all key-values
            else:
                return values
        except Exception as e:
            self.log.exception('Got Exception in get_key_value '
                               'method {}'.format(e))

    def assert_key_value(self):
        pass

    def set_key_value(self):
        pass
