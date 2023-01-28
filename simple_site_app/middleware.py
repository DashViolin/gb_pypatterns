from datetime import date


def date_middleware(request: dict):
    request["date"] = date.today()
