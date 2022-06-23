from loguru import logger

logger.add('out.log', backtrace=True, diagnose=True)