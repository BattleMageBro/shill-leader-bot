import os
from dotenv import load_dotenv, dotenv_values
from logg import log

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
a = False
config = {}

if os.path.exists(dotenv_path):
    a = load_dotenv(dotenv_path)
if a:
    config = dotenv_values(".env")

log.debug(config)
