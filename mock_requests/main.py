import requests
from requests.auth import HTTPBasicAuth


def resp():
    """
    Return the response of a GET request.
    """
    resp = requests.get("https://static-website.com")
    resp.raise_for_status()
    return resp


def text():
    """
    Return the content of a response in unicode.
    """
    resp = requests.get("https://static-website.com")
    resp.raise_for_status()
    return resp.text


def json():
    """
    Return the JSON-encoded content of a response.
    """
    resp = requests.get("https://static-website.com")
    resp.raise_for_status()
    return resp.json()


def auth():
    """
    Return the JSON-encoded content of a response.

    Attaches HTTP Basic authentication to the Request object.
    """
    basic = HTTPBasicAuth("user", "password")
    resp = requests.get("https://static-website.com", auth=basic)
    resp.raise_for_status()
    return resp.json()
