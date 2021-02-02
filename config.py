import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S')

log = logger = logging
api_key = os.environ['API_KEY']
conn_str = os.environ['CONNECTION_STRING']