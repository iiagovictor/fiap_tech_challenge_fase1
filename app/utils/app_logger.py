import logging
from app.models.logger import LoggerModel

class AppLogger():
    def create_logger(self, name):
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        
        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False
        return logger
    
    def set_log_message(self, logger, body: LoggerModel):
        type = body.get('type', 'info')
        
        if type == 'info':
            logger.info(body)
        elif type == 'error':
            logger.error(body)
        elif type == 'warning':
            logger.warning(body)