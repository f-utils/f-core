import logging
from logging.handlers import RotatingFileHandler

class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[95m',
        'DONE': '\033[33m'
    }
    RESET_CODE = '\033[0m'

    LEVEL_NAME_MAPPING = {
        'DEBUG': 'log',
        'INFO': 'inf',
        'WARNING': 'wrn',
        'ERROR': 'err',
        'CRITICAL': 'crt',
        'DONE': 'ok!'
    }

    def format(self, record):
        original_levelname = record.levelname
        if record.levelname in self.LEVEL_NAME_MAPPING:
            record.levelname = self.LEVEL_NAME_MAPPING[record.levelname]
        log_record_format = '%(asctime)s | %(levelname)s | %(message)s'
        self._style._fmt = log_record_format
        self.datefmt = '%H:%M | %d/%m/%Y'

        original_format = super().format(record)

        record.levelname = original_levelname
        color_code = self.COLOR_CODES.get(record.levelname, self.RESET_CODE)

        return f'{color_code}{original_format}{self.RESET_CODE}'

def custom_level(name, number, color, abbrev):
    logging.addLevelName(number, name.upper())

    def log_method(self, message, *args, **kws):
        if self.isEnabledFor(number):
            self._log(number, message, args, **kws)

    setattr(logging.Logger, name.lower(), log_method)
    ColoredFormatter.COLOR_CODES[name.upper()] = color
    ColoredFormatter.LEVEL_NAME_MAPPING[name.upper()] = abbrev

custom_level('DONE', 15, '\033[33m', 'ok!')
logger = None

LOG_LEVELS_STR_MAP = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def init(name='logs', level='debug', file=None, mb=1, bkps=1):
    global logger
    logger = logging.getLogger(name)
    if isinstance(level, str):
        level = LOG_LEVELS_STR_MAP.get(level.lower(), logging.DEBUG)
    if not logger.hasHandlers():
        logger.setLevel(level)
        console_handler = logging.StreamHandler()
        formatter = ColoredFormatter()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        if file:
            max_bytes = mb * 1024 * 1024
            file_handler = RotatingFileHandler(
                file, maxBytes=max_bytes, backupCount=bkps)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        logger.propagate = False

def log(message, *args):
    logger.debug(message, *args)
def inf(message, *args):
    logger.info(message, *args)
def ok(message, *args):
    logger.done(message, *args)
def err(message, *args):
    logger.error(message, *args)
def wrn(message, *args):
    logger.warning(message, *args)

def new_log(name, number, color, abbrev):
    custom_level(name, number, color, abbrev)
    def log_method(message, *args):
        getattr(logger, name.lower())(message, *args)
    globals()[name.lower()] = log_method
