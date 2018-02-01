import os
import logging
import datetime
import time
from logging.handlers import RotatingFileHandler
from common_lib import parse_yaml


class Rest_Logger():
    time_value = time.time()
    tf = datetime.datetime.fromtimestamp(
        time_value).strftime('%Y-%m-%d_%H-%M-%S')
    conf_obj = parse_yaml.Yamlparser()
    yaml_data = conf_obj.get_data()
    log_levels = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40,
                  'CRITICAL': 50, 'OFF': 0}

    def __init__(self):
        # Getting log_type, creating filename and log formt
        self.log_level = self.log_levels[self.yaml_data['log_level']]
        self.dir = self.yaml_data['log_directory']
        if self.dir:
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
            self.filename = self.dir+str(self.tf)+'.log'
            self.file = os.path.abspath(self.filename)
        else:
            self.filename = '../pyRest_logs/pyrestlogs_'+str(self.tf)+'.log'
            self.file = os.path.abspath(self.filename)
        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - ' \
                          '%(message)s'

    def get_logger(self, name):
        try:
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
            rh.setLevel(self.log_level)
            # add the handlers to logger
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.addHandler(rh)
            return self.logger
        except Exception as e:
            self.logger.exception("Error occured in logger function")
