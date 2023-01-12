def secret_front(request: dict):
    request["secret"] = "some secret"


def other_front(request: dict):
    request["key"] = "key"
