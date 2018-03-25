import os,sys
import logging
import datetime
import time
from logging.handlers import RotatingFileHandler
from common_lib import parse_yaml


class Rest_Logger():
    time_value = time.time()
    tf = datetime.datetime.fromtimestamp(
        time_value).strftime('%Y-%m-%d_%H-%M-%S')
    cw = os.getcwd()
    b = os.path.join(cw,'resources')
    # log_config = os.path.abspath('../pyRestAuto/resources/logging.yaml')
    log_config = b+'//logging.yaml'
    conf_obj = parse_yaml.Yamlparser(filename=log_config)
    yaml_data = conf_obj.get_data()
    print(yaml_data,'logging config data')
    log_levels = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40,
                  'CRITICAL': 50, 'OFF': 0}

    def __init__(self):
        # Getting log_type, creating filename and log format
        self.log_level = self.log_levels[self.yaml_data['log_level']]
        self.dir = self.yaml_data['log_directory']
        # Checking and creating dir if not present
        if self.dir:
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
            self.filename = self.dir+str(self.tf)+'.log'
            self.file = os.path.abspath(self.filename)
        else:
            print('in else')
            # Checking and creating pyRest_logs dir if not present
            self.dir1 = os.path.join(self.cw,'pyRest_logs')
            print(self.dir1,'logs dir')
            # self.dir1 = os.path.abspath('../pyRestAuto/pyRest_logs/')
            if not os.path.exists(self.dir1):
                os.makedirs(self.dir1)
            self.filename = self.dir1+'/pyrestlogs_'+str(self.tf)+'.log'
            self.file = os.path.abspath(self.filename)
            print(self.file)
        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - ' \
                          '%(message)s'

    def get_logger(self, name):
        try:
            print(name)
            self.logger = logging.getLogger(name)
            self.logger.setLevel(self.log_level)
            # create file handler which logs even debug messages
            fh = logging.FileHandler(self.file)
            fh.setLevel(self.log_level)
            # create console handler with a higher log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.ERROR)
            # create formatter and add it to the handlers
            formatter = logging.Formatter(self.log_format)
            ch.setFormatter(formatter)
            fh.setFormatter(formatter)
            rh = RotatingFileHandler(self.filename, maxBytes=10000,
                                     backupCount=1)
            rh.setLevel(logging.ERROR)
            # add the handlers to logger
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.addHandler(rh)
            return self.logger
        except Exception as e:
            self.logger.exception("Error occured in logger function {}".format(e))
