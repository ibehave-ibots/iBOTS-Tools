import urllib.parse


def double_encoder(uuid):
    uuid_single_encode = urllib.parse.quote_plus(uuid)
    return (urllib.parse.quote_plus(uuid_single_encode))
