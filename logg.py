from loguru import logger

log = logger
log.add('out.log', backtrace=True, diagnose=True)