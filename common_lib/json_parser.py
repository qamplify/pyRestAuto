import simplejson as json
import traceback


class JsonParser(object):
    def __init__(self):
        pass

    def validate_json(self):
        """
        Checks if json is valid or not.
        returns True if valid, else False
        :return:
        """
        pass

    def load_json_data(self, data):
        try:
            return json.loads(data)
        except Exception as e:
            print("Got exception when load json data {}".format(data))
            traceback.print_exc()

    def dump_json_data(self, data):
        #Returning python data type
        return json.dumps(data)

    def parse(self):
        pass

    def get_key_value(self):
        pass

    def assert_key_value(self):
        pass

    def set_key_value(self):
        pass
