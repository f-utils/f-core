import logging
from logging.handlers import RotatingFileHandler
from .ansi import *

class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        'DEBUG': bright_blue_,
        'INFO': bright_green_,
        'WARNING': bright_yellow_,
        'ERROR': bright_red_,
        'CRITICAL': bright_magenta_,
        'DONE': yellow_
    }

    LEVEL_NAME_MAPPING = {
        'DEBUG': 'log',
        'INFO': 'inf',
        'WARNING': 'wrn',
        'ERROR': 'err',
        'CRITICAL': 'crt',
        'DONE': 'ok!'
    }

    def __init__(self, log_format=None, date_format=None):
        super().__init__(log_format or '%(asctime)s | %(levelname)s | %(message)s', 
                         datefmt=date_format or '%H:%M | %d/%m/%Y')

    def format(self, record):
        original_levelname = record.levelname
        if record.levelname in self.LEVEL_NAME_MAPPING:
            record.levelname = self.LEVEL_NAME_MAPPING[record.levelname]

        original_format = super().format(record)

        record.levelname = original_levelname
        colored_message = self.COLOR_CODES.get(record.levelname, lambda x: x)(original_format)

        return colored_message

def custom_log_level(name, number, color, abbrev):
    logging.addLevelName(number, name.upper())

    def log_method(self, message, *args, **kws):
        if self.isEnabledFor(number):
            self._log(number, message, args, **kws)

    setattr(logging.Logger, name.lower(), log_method)
    ColoredFormatter.COLOR_CODES[name.upper()] = ansi_color_(color)
    ColoredFormatter.LEVEL_NAME_MAPPING[name.upper()] = abbrev

custom_log_level('DONE', 16, ANSI_COLORS['YELLOW'], 'ok!')
logger = None

LOG_LEVELS_STR_MAP = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def init_logs(
        name='logs',
        level='debug',
        log_format=None,
        date_format=None,
        file=None,
        mb=2,
        bkps=1
    ):
    global logger
    logger = logging.getLogger(name)
    if isinstance(level, str):
        level = LOG_LEVELS_STR_MAP.get(level.lower(), logging.DEBUG)
    if not logger.hasHandlers():
        logger.setLevel(level)
        console_handler = logging.StreamHandler()
        formatter = ColoredFormatter(log_format, date_format)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        if file:
            max_bytes = mb * 1025 * 1024
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
    custom_log_level(name, number, color, abbrev)
    def log_method(message, *args):
        getattr(logger, name.lower())(message, *args)
    globals()[name.lower()] = log_method
