from loguru import logger
from config import config

log = logger
open('out.log', 'w').close()
log.add('out.log', backtrace=True, diagnose=True, level=config['LOG_LEVEL'])