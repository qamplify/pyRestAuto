from common_lib.parse_yaml import Yamlparser
import yaml

def parse_test_data():
    with open("../resources/testdata.yaml",'r') as stream:
        print (yaml.load(stream))



if __name__ == '__main__':
    parse_test_data()