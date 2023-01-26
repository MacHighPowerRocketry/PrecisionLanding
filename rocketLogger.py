"""
Logging

Debug logs (code erorrs, warnings, ect, usefull for debugging code)

Data logging (sensor data, ect)

Main class would import the rocketLogger class, then call either dataLog(data_to_log) or debugLog(debug_to_log) depending on the context (logging sensor data or code issues)

"""

import logging


class rocketLogger:
    def __init__(self):
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.dataLogger = self.setup_logger('data_logger', 'logs/data.log', logging.INFO)
        self.debugLogger = self.setup_logger('debug_logger', 'logs/debug.log')

    def setup_logger(self, name, log_file, level=logging.WARNING):
        handler = logging.FileHandler(log_file)
        handler.setFormatter(self.formatter)

        logger = logging.getLogger("logs//" + name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    def dataLog(self,data_to_log):
        #Data log should probably always be info level
        self.dataLogger.info(data_to_log)
    
    def debugLog(self, debug_to_log, level=logging.WARNING):
        self.debugLogger.log(level, debug_to_log)


