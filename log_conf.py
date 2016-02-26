import logging.config

def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()

@singleton
class Logger():
    def __init__(self):
        logging.config.fileConfig('config.cfg')
        self.logr = logging.getLogger('Video Cleaner')
