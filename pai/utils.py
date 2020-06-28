import hashlib


def md5_digest(raw_data):
    return hashlib.md5(raw_data).hexdigest()
