import yaml
import os


class Yamlparser():
    """
    Initiate this class object with yaml file path
    Usage:
        path = os.path.abspath("../resources/config.yaml")
        obj = Yamlparser(path)
    """

    def __init__(self, filename=None):
        if filename:
            self.file = filename
        else:
            self.file = os.path.abspath('../resources/config.yaml')

    def get_data(self):
        """
        This method is used to get data from yaml file.
        :param root: YAML file root name
        :param branch: YAML branch name
        :return:
        """
        try:
            with open(self.file, 'r') as yamlfile:
                data = yaml.load(yamlfile)
                return data
        except Exception as e:
            print("Error occured in configuration file {}".format(self.file))


# test = Yamlparser()
# a=test.get_data(branch='auth_details')
# print (a,type(a))
