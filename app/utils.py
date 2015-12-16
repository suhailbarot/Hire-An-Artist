import hashlib
from app.constants import SALT
import datetime


def generate_hash(content):
    return str(hashlib.md5(content+SALT+str(datetime.datetime.now())).hexdigest())