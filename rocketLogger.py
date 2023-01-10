"""
Logging

Debug logs (code erorrs, warnings, ect, usefull for debugging code)

Data logging (sensor data, ect)

Main class would import the rocketLogger class, then call either dataLog(data_to_log) or debugLog(debug_to_log) depending on the context (logging sensor data or code issues)

"""

import logging


class rocketLogger:
    def __init__(self):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.dataLogger = setup_logger('data_logger', 'data.log', logging.INFO)
        self.debugLogger = setup_logger('debug_logger', 'debug.log')


    def setup_logger(name, log_file, level=logging.WARNING):
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    def dataLog(data_to_log):
        #Data log should probably always be info level
        self.dataLoggger.info(data_to_log)
    
    def debugLog(level=logging.WARNING, debug_to_log)
        self.debugLogger.log(level, debug_to_log)


